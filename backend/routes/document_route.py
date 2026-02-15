from flask import Blueprint, send_file

document_bp = Blueprint('document_bp', __name__, url_prefix='/api/document')

@document_bp.route('/interface', methods=['GET'])
def getIterfaceDocument():
    # Send the PDF file directly to the frontend
    return send_file('./static/Interface_Document.pdf', as_attachment=False, mimetype='application/pdf')
