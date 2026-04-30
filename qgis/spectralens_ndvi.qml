<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<!--
  SpectraLens NDVI pseudocolor style for QGIS.
  Drop next to spectralens_ndvi.tif and QGIS will load it automatically,
  or apply via: Layer Properties > Symbology > Style > Load Style.
-->
<qgis version="3.34.0" hasScaleBasedVisibilityFlag="0" minScale="1e+08" maxScale="0" styleCategories="AllStyleCategories">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <pipe>
    <provider>
      <resampling enabled="false" zoomedInResamplingMethod="nearestNeighbour" zoomedOutResamplingMethod="nearestNeighbour" maxOversampling="2"/>
    </provider>
    <rasterrenderer band="1" type="singlebandpseudocolor" alphaBand="-1" classificationMin="-0.2" classificationMax="0.9" opacity="1" nodataColor="">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>None</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" classificationMode="1" minimumValue="-0.2" maximumValue="0.9" clip="0" labelPrecision="2">
          <colorramp name="[source]" type="gradient">
            <Option type="Map">
              <Option type="QString" name="color1" value="165,0,38,255"/>
              <Option type="QString" name="color2" value="0,104,55,255"/>
              <Option type="QString" name="discrete" value="0"/>
              <Option type="QString" name="rampType" value="gradient"/>
              <Option type="QString" name="stops" value="0.1;215,48,39,255:0.2;244,109,67,255:0.3;253,174,97,255:0.4;254,224,139,255:0.5;255,255,191,255:0.6;217,239,139,255:0.7;166,217,106,255:0.8;102,189,99,255:0.9;26,152,80,255"/>
            </Option>
          </colorramp>
          <item alpha="255" label="Bare / pest -0.20" color="#a50026" value="-0.2"/>
          <item alpha="255" label="Severe stress -0.05" color="#d73027" value="-0.05"/>
          <item alpha="255" label="Stressed 0.10" color="#f46d43" value="0.1"/>
          <item alpha="255" label="Sparse 0.25" color="#fdae61" value="0.25"/>
          <item alpha="255" label="Moderate 0.40" color="#fee08b" value="0.4"/>
          <item alpha="255" label="Healthy 0.55" color="#a6d96a" value="0.55"/>
          <item alpha="255" label="Vigorous 0.70" color="#66bd63" value="0.7"/>
          <item alpha="255" label="Dense canopy 0.90" color="#006837" value="0.9"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast brightness="0" gamma="1" contrast="0"/>
    <huesaturation invertColors="0" saturation="0" colorizeStrength="100" colorizeOn="0" colorizeBlue="128" colorizeRed="255" colorizeGreen="128" grayscaleMode="0"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
