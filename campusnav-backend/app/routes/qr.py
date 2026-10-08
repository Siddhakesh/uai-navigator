"""
QR Code API Blueprint
Generates QR codes for campus checkpoints.
"""
import io
import base64
import qrcode
from qrcode.image.svg import SvgImage
from flask import Blueprint, request, jsonify, send_file
from app import mongo

bp = Blueprint("qr", __name__)


def generate_qr_image(url, format="PNG", box_size=10, border=4):
    """Generate a QR code image for the given URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    if format.upper() == "SVG":
        img = qr.make_image(image_factory=SvgImage)
        buffer = io.BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return buffer, "image/svg+xml"
    else:
        img = qr.make_image(fill_color="#1e1b4b", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer, "image/png"


@bp.route("/qr/generate", methods=["POST"])
def generate_qr():
    """Generate a QR code for a checkpoint."""
    data = request.get_json()
    checkpoint_id = data.get("checkpoint_id")
    base_url = data.get("base_url", "https://campusnav.uai.edu.in")
    fmt = data.get("format", "PNG").upper()
    as_base64 = data.get("base64", False)

    if not checkpoint_id:
        return jsonify({"error": "checkpoint_id is required"}), 400

    # Check checkpoint exists
    cp = mongo.db.checkpoints.find_one({"checkpoint_id": checkpoint_id})
    if not cp:
        return jsonify({"error": f"Checkpoint '{checkpoint_id}' not found"}), 404

    nav_url = f"{base_url}/navigate?checkpoint={checkpoint_id}"

    buffer, mime = generate_qr_image(nav_url, format=fmt)

    if as_base64:
        encoded = base64.b64encode(buffer.read()).decode("utf-8")
        return jsonify({
            "checkpoint_id": checkpoint_id,
            "checkpoint_name": cp["name"],
            "url": nav_url,
            "format": fmt,
            "data": f"data:{mime};base64,{encoded}",
        })

    return send_file(
        buffer,
        mimetype=mime,
        as_attachment=True,
        download_name=f"qr_{checkpoint_id}.{fmt.lower()}",
    )


@bp.route("/qr/sheet", methods=["GET"])
def qr_sheet():
    """Generate data for a printable QR sheet of all checkpoints."""
    base_url = request.args.get("base_url", "https://campusnav.uai.edu.in")
    checkpoints = list(mongo.db.checkpoints.find({"is_active": True}))

    qr_data = []
    for cp in checkpoints:
        nav_url = f"{base_url}/navigate?checkpoint={cp['checkpoint_id']}"
        buffer, mime = generate_qr_image(nav_url, box_size=8, border=3)
        encoded = base64.b64encode(buffer.read()).decode("utf-8")
        qr_data.append({
            "checkpoint_id": cp["checkpoint_id"],
            "name": cp["name"],
            "description": cp.get("description", ""),
            "floor": cp.get("floor", 0),
            "type": cp.get("type", "checkpoint"),
            "url": nav_url,
            "qr_image": f"data:{mime};base64,{encoded}",
        })

    return jsonify({
        "base_url": base_url,
        "total": len(qr_data),
        "checkpoints": qr_data,
    })


@bp.route("/qr/preview/<checkpoint_id>", methods=["GET"])
def preview_qr(checkpoint_id):
    """Preview QR code as PNG for a given checkpoint."""
    base_url = request.args.get("base_url", "https://campusnav.uai.edu.in")
    fmt = request.args.get("format", "PNG").upper()

    cp = mongo.db.checkpoints.find_one({"checkpoint_id": checkpoint_id})
    if not cp:
        return jsonify({"error": "Checkpoint not found"}), 404

    nav_url = f"{base_url}/navigate?checkpoint={checkpoint_id}"
    buffer, mime = generate_qr_image(nav_url, format=fmt)

    return send_file(buffer, mimetype=mime)
