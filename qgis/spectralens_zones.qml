<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<!--
  SpectraLens zone-classification style for QGIS.
  Categorized renderer keyed off the "classification" attribute, with labels
  showing zone_id + mean_ndvi. Drop next to spectralens_zones.geojson or
  apply via Layer Properties > Symbology > Style > Load Style.
-->
<qgis version="3.34.0" simplifyAlgorithm="0" simplifyDrawingHints="1" simplifyMaxScale="1" simplifyDrawingTol="1" simplifyLocal="1" labelsEnabled="1" styleCategories="AllStyleCategories">
  <renderer-v2 type="categorizedSymbol" attr="classification" enableorderby="0" forceraster="0" symbollevels="0">
    <categories>
      <category render="true" symbol="0" label="Healthy" value="Healthy"/>
      <category render="true" symbol="1" label="Nitrogen Deficient" value="Nitrogen Deficient"/>
      <category render="true" symbol="2" label="Water Stressed" value="Water Stressed"/>
      <category render="true" symbol="3" label="Pest Damage" value="Pest Damage"/>
      <category render="true" symbol="4" label="Other" value=""/>
    </categories>
    <symbols>
      <symbol type="fill" name="0" alpha="0.6" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <Option type="Map">
            <Option type="QString" name="color" value="38,140,67,153"/>
            <Option type="QString" name="outline_color" value="0,0,0,255"/>
            <Option type="QString" name="outline_width" value="0.5"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
        </layer>
      </symbol>
      <symbol type="fill" name="1" alpha="0.6" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <Option type="Map">
            <Option type="QString" name="color" value="241,196,15,153"/>
            <Option type="QString" name="outline_color" value="0,0,0,255"/>
            <Option type="QString" name="outline_width" value="0.5"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
        </layer>
      </symbol>
      <symbol type="fill" name="2" alpha="0.6" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <Option type="Map">
            <Option type="QString" name="color" value="230,126,34,153"/>
            <Option type="QString" name="outline_color" value="0,0,0,255"/>
            <Option type="QString" name="outline_width" value="0.5"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
        </layer>
      </symbol>
      <symbol type="fill" name="3" alpha="0.6" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <Option type="Map">
            <Option type="QString" name="color" value="192,57,43,153"/>
            <Option type="QString" name="outline_color" value="0,0,0,255"/>
            <Option type="QString" name="outline_width" value="0.5"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
        </layer>
      </symbol>
      <symbol type="fill" name="4" alpha="0.6" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" pass="0" enabled="1" locked="0">
          <Option type="Map">
            <Option type="QString" name="color" value="149,165,166,153"/>
            <Option type="QString" name="outline_color" value="0,0,0,255"/>
            <Option type="QString" name="outline_width" value="0.5"/>
            <Option type="QString" name="style" value="solid"/>
          </Option>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
  <labeling type="simple">
    <settings>
      <text-style fontFamily="Arial" fontSize="10" fontWeight="75" textColor="0,0,0,255" fieldName="concat('Zone ', &quot;zone_id&quot;, ' — NDVI ', round(&quot;mean_ndvi&quot;, 2))" isExpression="1"/>
      <text-buffer bufferDraw="1" bufferSize="1" bufferColor="255,255,255,255"/>
      <placement placement="1"/>
    </settings>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
</qgis>
