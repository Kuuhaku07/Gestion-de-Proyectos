import random
import string
import hashlib
import os
import shutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def hash_text(text):
    encoded_text = text.encode()
    hash_object = hashlib.sha256(encoded_text)
    hash_hex = hash_object.hexdigest()
    return hash_hex

def generar_clave(longitud=32):
    """Genera una clave aleatoria de longitud especificada."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    clave = ''.join(random.choice(caracteres) for _ in range(longitud))
    return clave

def xor_encrypt_decrypt(text, key):
    #  Encriptar o desencriptar texto usando XOR
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

def almacenar_pdf(pdf_path, key):
    # Define the target directory
    target_directory = 'data/pdf'
    
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # Get the filename from the provided path
    filename = os.path.basename(pdf_path)
    
    # Define the target path for the encrypted PDF
    target_path = os.path.join(target_directory, filename + '.enc')  # Save as .enc for encrypted file
    
    # Read the PDF file as binary
    with open(pdf_path, 'rb') as file:
        pdf_data = file.read()
    
    # Encrypt the PDF data
    encrypted_data = xor_encrypt_decrypt(pdf_data.decode('latin-1'), key)  # Decode to string for XOR
    
    # Save the encrypted data to the target path
    with open(target_path, 'wb') as file:
        file.write(encrypted_data.encode('latin-1'))  # Encode back to bytes for saving
    
    return target_path


def descargar_pdf(encrypted_pdf_path, key, output_path=None):
    # Set default output path to the user's Downloads directory if not provided
    if output_path is None:
        output_path = os.path.join(os.path.expanduser("~"), "Downloads", os.path.basename(encrypted_pdf_path[:-4]))  # Remove .enc extension
    else:
        # Si se proporciona output_path, asegurarse de que sea un directorio y agregar el nombre del archivo
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, os.path.basename(encrypted_pdf_path[:-4]))  # Remove .enc extension
    
    # Read the encrypted PDF file as binary
    with open(encrypted_pdf_path, 'rb') as file:
        encrypted_data = file.read()
    
    # Decrypt the PDF data
    decrypted_data = xor_encrypt_decrypt(encrypted_data.decode('latin-1'), key)  # Decode to string for XOR
    
    # Save the decrypted data to the specified output path
    with open(output_path, 'wb') as file:
        file.write(decrypted_data.encode('latin-1'))  # Encode back to bytes for saving
    
    return output_path
def generar_reporte_proyecto(proyecto_id, output_path=None):
    """Genera un PDF con información de documentos de un proyecto"""
    # Set default output path to Downloads if not provided
    if output_path is None:
        output_path = os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        # If output_path is provided, ensure it's a directory and add filename
        if os.path.isdir(output_path):
            pass  # Use as-is
        else:
            # If it's a file path, extract directory and create it
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            return output_path  # Return the full file path
    
    # Crear documento en orientación horizontal (landscape)
    from reportlab.lib.pagesizes import landscape
    from database import obtener_proyecto_completo
    
    # Obtener datos del proyecto
    datos_proyecto = obtener_proyecto_completo(proyecto_id)
    if not datos_proyecto:
        print(f"Error: No se encontró el proyecto con ID {proyecto_id}")
        return None
    
    proyecto = datos_proyecto['proyecto']
    nombre_archivo = f"{proyecto[5]}_{proyecto[1]}.pdf".replace(" ", "_")
    ruta_completa = os.path.join(output_path, nombre_archivo)
    # Crear directorio si no existe
    os.makedirs(output_path, exist_ok=True)
    doc = SimpleDocTemplate(ruta_completa, pagesize=landscape(letter))
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    

    if not datos_proyecto:
        print(f"Error: No se encontró el proyecto con ID {proyecto_id}")
        return None
    
    proyecto = datos_proyecto['proyecto']
    
    # Encabezado con manejo robusto de errores para el logo
    try:
        logo = Image("logo_pdvsa.png", width=1.5*inch, height=0.75*inch)
        # Verificar que el archivo existe realmente
        if not os.path.exists("logo_pdvsa.png"):
            raise FileNotFoundError
        header_table = Table([
            [logo, Paragraph("PDVSA<br/>Sistema de Gestión Documental", styles['Heading2'])]
        ], colWidths=[2*inch, 6*inch])
        elements.append(header_table)
    except Exception as e:
        # Si falla el logo, usar versión simple de texto
        header_style = styles['Heading1']
        header_style.textColor = colors.HexColor('#CC0000')
        header = Paragraph("PDVSA - Sistema de Gestión Documental", header_style)
        elements.append(header)

    
    # Línea separadora
    elements.append(Spacer(1, 0.1*inch))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CC0000'), spaceBefore=5, spaceAfter=15))
    
    # Título del reporte 
    titulo_style = styles['Heading1']
    titulo_style.textColor = colors.HexColor('#003366')  # Azul oscuro corporativo
    titulo_style.alignment = 1  # Centrado
    titulo_style.fontSize = 18
    titulo_style.leading = 24  # Espaciado entre líneas
    titulo = Paragraph(
        f"Reporte del Proyecto: {proyecto[5]} - {proyecto[1]} (Cliente: {proyecto[4]})", 
        titulo_style
    )
    elements.append(titulo)
    
    # Tabla resumen de revisiones (alineada a la derecha)
    rev_counts = {'Rev A': 0, 'Rev B': 0, 'Rev 0': 0}
    for doc_data in datos_proyecto['documentos']:
        revision = doc_data['documento'][7]  # Campo de revisión
        if revision in rev_counts:
            rev_counts[revision] += 1
    
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    
    # Importaciones necesarias para el layout
    from reportlab.platypus import KeepTogether
    
    # Calcular altura dinámica basada en cantidad de datos
    max_value = max(rev_counts.values())
    chart_height = min(150 + (max_value * 5), 300)  # Altura entre 150-300px
    
    # Crear gráfico de barras adaptable
    drawing = Drawing(250, chart_height)
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 20
    bc.height = chart_height - 40
    bc.width = 150
    bc.data = [[v for v in rev_counts.values()]]
    bc.strokeColor = colors.black
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max_value * 1.2  # Margen superior
    bc.barSpacing = 0.2
    bc.barWidth = 3
    bc.bars[0].fillColor = colors.HexColor('#1f77b4')  # Azul más profesional
    bc.categoryAxis.categoryNames = list(rev_counts.keys())
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 0
    drawing.add(bc)

    # Crear tabla resumen
    resumen_data = [["Revisión", "Cantidad"]]
    resumen_data.extend([[k, str(v)] for k, v in rev_counts.items()])
    
    # Crear tabla con estilo mejorado
    resumen_table = Table(resumen_data, colWidths=[inch*1.5, inch*1])
    resumen_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f7f7f7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ])
    resumen_table.setStyle(resumen_style)

    # Crear layout flexible usando Table
    container = Table([
        [drawing, resumen_table]
    ], colWidths=['40%', '60%'],
    style=TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (0,0), 20),  # Espacio izquierdo para el gráfico
        ('RIGHTPADDING', (1,0), (1,0), 10)  # Espacio derecho para la tabla
    ]))
    
    # Agregar al documento con espaciado
    elements.append(Spacer(1, 0.3*inch))
    elements.append(container)
    elements.append(Spacer(1, 0.4*inch))
    
    
    

    
    # Encabezados de tabla
    encabezados = [
        "Disciplina", 
        "Código", 
        "Nombre",
        "Revisión", 
        "Status",
        "Emisión",
        "Recepción"
    ]
    
    # Preparar datos para la tabla
    data = [encabezados]
    
    for doc_data in datos_proyecto['documentos']:
        documento = doc_data['documento']
        
        # Manejar documentos sin versiones
        if not doc_data['versiones']:
            # Mostrar documento con datos básicos y campos vacíos para versiones
            data.append([
                Paragraph(documento[5], styles['Normal']),  # Disciplina
                Paragraph(f"{proyecto[5]}-{documento[2]}", styles['Normal']),  # Código sin transmittal
                Paragraph(documento[3], styles['Normal']),  # Nombre
                Paragraph(documento[7], styles['Normal']),  # Revisión
                Paragraph("-", styles['Normal']),  # Status vacío
                Paragraph("-", styles['Normal']),  # Emisión vacía
                Paragraph("-", styles['Normal'])  # Recepción vacía
            ])
            continue

        # Buscar versión que coincida con la revisión del documento
        version_actual = None
        for version in doc_data['versiones']:
            if version['version'][2] == documento[7]:  # Comparar nombre versión con revisión doc
                version_actual = version
                break
        
        if not version_actual:
            # Mostrar documento con revisión pero sin versión coincidente
            data.append([
                Paragraph(documento[5], styles['Normal']),  # Disciplina
                Paragraph(f"{proyecto[5]}-{documento[2]}", styles['Normal']),  # Código sin transmittal
                Paragraph(documento[3], styles['Normal']),  # Nombre
                Paragraph(documento[7], styles['Normal']),  # Revisión
                Paragraph("(No coincide)", styles['Normal']),  # Status
                Paragraph("-", styles['Normal']),  # Emisión
                Paragraph("-", styles['Normal'])  # Recepción
            ])
            continue
            
        # Buscar fechas de emisión y recepción
        fecha_emision = fecha_recepcion = None
        for fecha in version_actual['fechas']:
            if fecha[2] == "Fecha de Emisión":
                fecha_emision = fecha[3]
            elif fecha[2] == "Fecha de Recepción":
                fecha_recepcion = fecha[3]
        
        # Construir código compuesto: proyecto-documento-transmitall
        codigo_compuesto = f"{proyecto[5]}-{documento[2]}-{version_actual['version'][5]}"
        
        # Agregar fila a la tabla
        data.append([
            Paragraph(documento[5], styles['Normal']),  # Disciplina
            Paragraph(codigo_compuesto, styles['Normal']),  # Código compuesto
            Paragraph(documento[3], styles['Normal']),  # Nombre
            Paragraph(documento[7], styles['Normal']),  # Revisión
            Paragraph(version_actual['version'][3], styles['Normal']),  # Status
            Paragraph(fecha_emision or "-", styles['Normal']),  # Emisión
            Paragraph(fecha_recepcion or "-", styles['Normal'])  # Recepción
        ])
    
    # Ajustar ancho de columnas para mejor uso del espacio horizontal
    col_widths = [inch*1.2, inch*2.0, inch*3.0, inch*1.0, inch*1.0, inch*1.0, inch*1.0]
    
    # Crear tabla con anchos personalizados
    tabla = Table(data, colWidths=col_widths)
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),  # Centrado vertical
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('LEADING', (0,0), (-1,-1), 14)  # Espaciado entre líneas
    ])
    tabla.setStyle(estilo_tabla)
    elements.append(tabla)
    
    # Generar PDF
    try:
        doc.build(elements)
        return ruta_completa
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        return None







def generar_reporte_rev0(proyecto_id, output_path=None):
    """Genera un PDF con documentos en Rev 0 y porcentaje de completitud"""
    # Set default output path to Downloads if not provided
    if output_path is None:
        output_path = os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        # If output_path is provided, ensure it's a directory and add filename
        if os.path.isdir(output_path):
            pass  # Use as-is
        else:
            # If it's a file path, extract directory and create it
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            return output_path  # Return the full file path
    
    from reportlab.lib.pagesizes import landscape
    from database import obtener_proyecto_completo
    
    # Obtener datos del proyecto
    datos_proyecto = obtener_proyecto_completo(proyecto_id)
    if not datos_proyecto:
        print(f"Error: No se encontró el proyecto con ID {proyecto_id}")
        return None
    
    proyecto = datos_proyecto['proyecto']
    nombre_archivo = f"Rev0_{proyecto[5]}_{proyecto[1]}.pdf".replace(" ", "_")
    ruta_completa = os.path.join(output_path, nombre_archivo)
    os.makedirs(output_path, exist_ok=True)
    
    # Crear documento (igual que en la otra función)
    doc = SimpleDocTemplate(ruta_completa, pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # Filtrar solo documentos en Rev 0
    docs_rev0 = [d for d in datos_proyecto['documentos'] if d['documento'][7] == 'Rev 0']
    total_docs = len(datos_proyecto['documentos'])
    porcentaje = (len(docs_rev0) / total_docs) * 100 if total_docs > 0 else 0

    # Encabezado (similar pero específico para Rev 0)
    try:
        logo = Image("logo_pdvsa.png", width=1.5*inch, height=0.75*inch)
        if not os.path.exists("logo_pdvsa.png"):
            raise FileNotFoundError
        header_table = Table([
            [logo, Paragraph("PDVSA<br/>Reporte Rev 0", styles['Heading2'])]
        ], colWidths=[2*inch, 6*inch])
        elements.append(header_table)
    except Exception as e:
        header_style = styles['Heading1']
        header_style.textColor = colors.HexColor('#CC0000')
        header = Paragraph("PDVSA - Reporte Rev 0", header_style)
        elements.append(header)
    
    elements.append(Spacer(1, 0.1*inch))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#CC0000'), spaceBefore=5, spaceAfter=15))
    
    # Título del reporte
    titulo_style = styles['Heading1']
    titulo_style.textColor = colors.HexColor('#003366')
    titulo_style.alignment = 1
    titulo = Paragraph(f"Reporte Rev 0: {proyecto[5]} - {proyecto[1]}", titulo_style)
    elements.append(titulo)
    
    # Porcentaje de completitud
    porcentaje_style = styles['Heading2']
    porcentaje_style.textColor = colors.HexColor('#006600')
    elements.append(Paragraph(f"Porcentaje completado: {porcentaje:.1f}%", porcentaje_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de documentos con ambas fechas
    encabezados = ["Código", "Transmittal", "Nombre", "Disciplina", "Emisión", "Recepción"]
    data = [encabezados]
    
    for doc_data in docs_rev0:
        documento = doc_data['documento']
        # Buscar ambas fechas (igual que en generar_reporte_proyecto)
        fecha_emision = fecha_recepcion = None
        transmitall = "-"
        if doc_data['versiones']:
            for version in doc_data['versiones']:
                for fecha in version['fechas']:
                    if fecha[2] == "Fecha de Emisión":
                        fecha_emision = fecha[3]
                    elif fecha[2] == "Fecha de Recepción":
                        fecha_recepcion = fecha[3]
                transmitall = version['version'][5] or "-"
        
        data.append([
            Paragraph(f"{proyecto[5]}-{documento[2]}", styles['Normal']),
            Paragraph(transmitall, styles['Normal']),
            Paragraph(documento[3], styles['Normal']),
            Paragraph(documento[5], styles['Normal']),
            Paragraph(fecha_emision or "-", styles['Normal']),
            Paragraph(fecha_recepcion or "-", styles['Normal'])
        ])
    
    tabla = Table(data, colWidths=[1.5*inch, 1.5*inch, 2.5*inch, 1.5*inch, 1.2*inch, 1.2*inch])
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    tabla.setStyle(estilo_tabla)
    elements.append(tabla)
    
    # Generar PDF (igual que en la otra función)
    try:
        doc.build(elements)
        return ruta_completa
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        return None
    

if __name__ == "__main__":
    # Test PDF generation with sample project ID
    result = generar_reporte_proyecto(1)
    if result:
        print(f"Reporte de proyecto generado como '{result}'")
    else:
        print("Error al generar el reporte")
