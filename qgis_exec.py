from PyQt5.QtGui import QColor
from datetime import datetime, timedelta
from qgis.core import QgsProject, QgsRuleBasedRenderer

layer_name = 'EMPREENDIMENTO'
layer_data = 'dt_licen_fim'
isReproved = 'licenc'

layer_res = QgsProject.instance().mapLayersByName(layer_name)[0]

# Get the index of the date field
index_data = layer_res.fields().indexFromName(layer_data)

index_reproved = field_names.index(isReproved)

index_reproved = layer_res.fields().indexFromName(isReproved)


# Get the current date as datetime.date
current_date = datetime.now().date()

# Define the orange alert interval (120 days before expiration)
orange_alert_interval = timedelta(days=120)

# Create a QgsRuleBasedRenderer object
renderer = QgsRuleBasedRenderer(QgsSymbol.defaultSymbol(layer_res.geometryType()))

# Create rules for Reproved features
rule_not_approved = QgsRuleBasedRenderer.Rule(QgsFillSymbol.defaultSymbol(layer_res.geometryType()))
rule_not_approved.setFilterExpression(f"\"{isReproved}\" = 'Não Aprovado'")
rule_not_approved.symbol().setColor(QColor(255, 0, 0))  # Red color
rule_not_approved.symbol().setOpacity(0.5)  # set opacity 50%

# Create rules for AProved features (garant)
rule_approved = QgsRuleBasedRenderer.Rule(QgsFillSymbol.defaultSymbol(layer_res.geometryType()))
rule_approved.setFilterExpression(f"\"{isReproved}\" = 'Aprovado'")
rule_approved.symbol().setColor(QColor(0, 255, 0))

# Create rules for expired and soon-to-expire features
rule_near = QgsRuleBasedRenderer.Rule(QgsFillSymbol.defaultSymbol(layer_res.geometryType()))
rule_near.setFilterExpression(f"\"{layer_data}\" >= '{current_date}' AND \"{layer_data}\" <= '{current_date + orange_alert_interval}'")  # Filter features soon-to-expire
rule_near.symbol().setColor(QColor(255, 165, 0))  # Orange color

rule_expired = QgsRuleBasedRenderer.Rule(QgsFillSymbol.defaultSymbol(layer_res.geometryType()))
rule_expired.setFilterExpression(f"\"{layer_data}\" < '{current_date}'")  # Filter expired features
rule_expired.symbol().setColor(QColor(255, 0, 0))  # Red for expired features
rule_expired.symbol().setOpacity(0.5)  # Set opacity to 50%

# Create the rule for OK features
rule_ok = QgsRuleBasedRenderer.Rule(QgsFillSymbol.defaultSymbol(layer_res.geometryType()))
rule_ok.setFilterExpression(f"\"{layer_data}\" >= '{current_date + orange_alert_interval}'")  # Filter OK features
rule_ok.symbol().setColor(QColor(0,255,0))  # Green for OK features

# Add the rules to the renderer in the desired order
renderer.rootRule().appendChild(rule_ok)
renderer.rootRule().appendChild(rule_near)
renderer.rootRule().appendChild(rule_expired)

# Guarantees red color setting in Unapproved cases
renderer.rootRule().appendChild(rule_not_approved)

# Set the renderer for the layer
layer_res.setRenderer(renderer)

# Refresh the canvas
iface.mapCanvas().refreshAllLayers()
