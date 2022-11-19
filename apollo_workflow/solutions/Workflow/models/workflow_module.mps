<?xml version="1.0" encoding="UTF-8"?>
<model ref="r:277ea055-6059-424a-8752-99e621b5bd87(workflow_module)">
  <persistence version="9" />
  <languages>
    <use id="ec3060ee-1f23-4e47-af80-3618736238b3" name="afcl.language" version="0" />
  </languages>
  <imports />
  <registry>
    <language id="ec3060ee-1f23-4e47-af80-3618736238b3" name="afcl.language">
      <concept id="3703551373945568696" name="afcl.language.structure.Data" flags="ng" index="02Hny">
        <child id="3703551373945568730" name="type" index="02Hm0" />
        <child id="3703551373945568729" name="value" index="02Hm3" />
      </concept>
      <concept id="3703551373945568695" name="afcl.language.structure.DataOutput" flags="ng" index="02HnH" />
      <concept id="3703551373945568692" name="afcl.language.structure.OutputBlock" flags="ng" index="02HnI">
        <child id="3703551373945568693" name="outputs" index="02HnJ" />
      </concept>
      <concept id="3703551373946370737" name="afcl.language.structure.FunctionType" flags="ng" index="07xbF" />
      <concept id="3703551373946370725" name="afcl.language.structure.FunctionStatement" flags="ng" index="07xbZ">
        <child id="3703551373946370743" name="type" index="07xbH" />
        <child id="3621437988970037615" name="dataIns" index="3uUYZ6" />
        <child id="3621437988970037616" name="dataOuts" index="3uUYZp" />
      </concept>
      <concept id="3703551373944476556" name="afcl.language.structure.StringType" flags="ng" index="0eRJm" />
      <concept id="3703551373944476557" name="afcl.language.structure.NumberType" flags="ng" index="0eRJn" />
      <concept id="3703551373948339761" name="afcl.language.structure.DataReference" flags="ng" index="0Z6TF">
        <reference id="3703551373948339762" name="scope" index="0Z6TC" />
        <reference id="3621437988967577453" name="dataReference" index="3uLpB4" />
      </concept>
      <concept id="8811045998705258" name="afcl.language.structure.LoopResultReference" flags="ng" index="22LnvN">
        <reference id="8811045998705261" name="scope" index="22LnvO" />
        <reference id="8811045998705263" name="reference" index="22LnvQ" />
      </concept>
      <concept id="8811045998705255" name="afcl.language.structure.LoopOutputBlock" flags="ng" index="22LnvY">
        <child id="8811045998705256" name="outputs" index="22LnvL" />
      </concept>
      <concept id="8811045999383196" name="afcl.language.structure.LoopDataInput" flags="ng" index="22YXW5" />
      <concept id="8811045999383164" name="afcl.language.structure.LoopInputBlock" flags="ng" index="22YXZ_">
        <child id="8811045999383165" name="inputs" index="22YXZ$" />
      </concept>
      <concept id="1564814548520487598" name="afcl.language.structure.ArrayType" flags="ng" index="2imxK$" />
      <concept id="1564814548518336754" name="afcl.language.structure.ForEachStatement" flags="ng" index="2iuMTS">
        <child id="8811045998705441" name="input" index="22LnqS" />
        <child id="8811045998705248" name="block" index="22LnvT" />
        <child id="8811045998705250" name="output" index="22LnvV" />
      </concept>
      <concept id="7318275687311091094" name="afcl.language.structure.Workflow" flags="ng" index="3j0p_w">
        <child id="3703551373946370745" name="input" index="07xbz" />
        <child id="3703551373946370748" name="output" index="07xbA" />
        <child id="7318275687311092959" name="body" index="3j0p0D" />
      </concept>
      <concept id="7318275687311091095" name="afcl.language.structure.InputBlock" flags="ng" index="3j0p_x">
        <child id="7318275687311101724" name="inputs" index="3j0vfE" />
      </concept>
      <concept id="7318275687311091096" name="afcl.language.structure.DataInput" flags="ng" index="3j0p_I" />
      <concept id="7318275687311091097" name="afcl.language.structure.BodyBlock" flags="ng" index="3j0p_J">
        <child id="3703551373946370752" name="statements" index="07xaq" />
      </concept>
      <concept id="3621437988972436302" name="afcl.language.structure.ResultReference" flags="ng" index="3uzRnB">
        <reference id="3621437988972436303" name="scope" index="3uzRnA" />
        <reference id="3621437988972436304" name="resultReference" index="3uzRnT" />
      </concept>
      <concept id="3621437988972568094" name="afcl.language.structure.ResultBlock" flags="ng" index="3u$n2R">
        <child id="3621437988972568097" name="results" index="3u$n28" />
      </concept>
      <concept id="4384759552460367937" name="afcl.language.structure.JsonInputLiteral" flags="ng" index="3xfQfl">
        <property id="4384759552460701842" name="value" index="3xcwG6" />
      </concept>
    </language>
    <language id="ceab5195-25ea-4f22-9b92-103b95ca8c0c" name="jetbrains.mps.lang.core">
      <concept id="1169194658468" name="jetbrains.mps.lang.core.structure.INamedConcept" flags="ng" index="TrEIO">
        <property id="1169194664001" name="name" index="TrG5h" />
      </concept>
    </language>
  </registry>
  <node concept="3j0p_w" id="6ULE2PD7rv7">
    <property role="TrG5h" value="ds_project" />
    <node concept="3j0p_J" id="6ULE2PD7rv8" role="3j0p0D">
      <node concept="07xbZ" id="6ULE2PD7r$i" role="07xaq">
        <property role="TrG5h" value="fetchImages" />
        <node concept="07xbF" id="6ULE2PD7r$s" role="07xbH">
          <property role="TrG5h" value="Fetch" />
        </node>
        <node concept="22YXZ_" id="6ULE2PD7r$k" role="3uUYZ6">
          <node concept="22YXW5" id="6ULE2PD7r_2" role="22YXZ$">
            <property role="TrG5h" value="bucket" />
            <node concept="0Z6TF" id="6ULE2PD7r_b" role="02Hm3">
              <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
              <ref role="3uLpB4" node="6ULE2PD7rw0" resolve="bucket" />
            </node>
          </node>
          <node concept="22YXW5" id="6ULE2PD7rEL" role="22YXZ$">
            <property role="TrG5h" value="batch_size" />
            <node concept="0Z6TF" id="6ULE2PD7rEZ" role="02Hm3">
              <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
              <ref role="3uLpB4" node="6ULE2PD7rxN" resolve="batch_size" />
            </node>
          </node>
        </node>
        <node concept="02HnI" id="6ULE2PD7r$l" role="3uUYZp">
          <node concept="02HnH" id="6ULE2PD7r_0" role="02HnJ">
            <property role="TrG5h" value="keys" />
            <node concept="2imxK$" id="6ULE2PD7r_n" role="02Hm0" />
          </node>
        </node>
      </node>
      <node concept="2iuMTS" id="6ULE2PD7r_v" role="07xaq">
        <property role="TrG5h" value="parralelFor" />
        <node concept="22YXZ_" id="6ULE2PD7r_x" role="22LnqS">
          <node concept="22YXW5" id="6ULE2PD7rDr" role="22YXZ$">
            <property role="TrG5h" value="iterator" />
            <node concept="0Z6TF" id="6ULE2PD7rEv" role="02Hm3">
              <ref role="0Z6TC" node="6ULE2PD7r$i" resolve="fetchImages" />
              <ref role="3uLpB4" node="6ULE2PD7r_0" resolve="keys" />
            </node>
          </node>
        </node>
        <node concept="3j0p_J" id="6ULE2PD7r_z" role="22LnvT">
          <node concept="07xbZ" id="6ULE2PD7r_U" role="07xaq">
            <property role="TrG5h" value="recognizeFaces" />
            <node concept="07xbF" id="6ULE2PD7r_V" role="07xbH">
              <property role="TrG5h" value="Recognize" />
            </node>
            <node concept="22YXZ_" id="6ULE2PD7r_W" role="3uUYZ6">
              <node concept="22YXW5" id="6ULE2PD7r_Y" role="22YXZ$">
                <property role="TrG5h" value="split_keys" />
                <node concept="0Z6TF" id="6ULE2PD7rA5" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7r_v" resolve="parralelFor" />
                  <ref role="3uLpB4" node="6ULE2PD7rDr" resolve="iterator" />
                </node>
              </node>
              <node concept="22YXW5" id="6ULE2PD7rAo" role="22YXZ$">
                <property role="TrG5h" value="bucket" />
                <node concept="0Z6TF" id="6ULE2PD7rAp" role="02Hm3">
                  <ref role="3uLpB4" node="6ULE2PD7rw0" resolve="bucket" />
                  <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
                </node>
              </node>
              <node concept="22YXW5" id="6ULE2PD7rF7" role="22YXZ$">
                <property role="TrG5h" value="emotions" />
                <node concept="0Z6TF" id="6ULE2PD7rFj" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
                  <ref role="3uLpB4" node="6ULE2PD7ryS" resolve="emotions" />
                </node>
              </node>
            </node>
            <node concept="02HnI" id="6ULE2PD7r_X" role="3uUYZp">
              <node concept="02HnH" id="6ULE2PD7rFq" role="02HnJ">
                <property role="TrG5h" value="detected_faces" />
                <node concept="2imxK$" id="6ULE2PD7rFv" role="02Hm0" />
              </node>
            </node>
          </node>
          <node concept="07xbZ" id="6ULE2PD7rFA" role="07xaq">
            <property role="TrG5h" value="cropSortFaces" />
            <node concept="07xbF" id="6ULE2PD7rFC" role="07xbH">
              <property role="TrG5h" value="CropSort" />
            </node>
            <node concept="22YXZ_" id="6ULE2PD7rFE" role="3uUYZ6">
              <node concept="22YXW5" id="6ULE2PD7rFI" role="22YXZ$">
                <property role="TrG5h" value="bucket" />
                <node concept="0Z6TF" id="6ULE2PD7rG0" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
                  <ref role="3uLpB4" node="6ULE2PD7rw0" resolve="bucket" />
                </node>
              </node>
              <node concept="22YXW5" id="6ULE2PD7rG7" role="22YXZ$">
                <property role="TrG5h" value="detected_faces" />
                <node concept="0Z6TF" id="6ULE2PD7rGn" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7r_U" resolve="recognizeFaces" />
                  <ref role="3uLpB4" node="6ULE2PD7rFq" resolve="detected_faces" />
                </node>
              </node>
              <node concept="22YXW5" id="6ULE2PD7rGu" role="22YXZ$">
                <property role="TrG5h" value="face_size" />
                <node concept="0Z6TF" id="6ULE2PD7rGz" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
                  <ref role="3uLpB4" node="6ULE2PD7rz_" resolve="face_size" />
                </node>
              </node>
            </node>
            <node concept="02HnI" id="6ULE2PD7rFG" role="3uUYZp">
              <node concept="02HnH" id="6ULE2PD7rOv" role="02HnJ">
                <property role="TrG5h" value="statusCode" />
                <node concept="0eRJn" id="6ULE2PD7rO$" role="02Hm0" />
              </node>
            </node>
          </node>
        </node>
        <node concept="22LnvY" id="6ULE2PD7r__" role="22LnvV">
          <node concept="22LnvN" id="6ULE2PD7rOC" role="22LnvL">
            <property role="TrG5h" value="statusCode" />
            <ref role="22LnvO" node="6ULE2PD7rFA" resolve="cropSortFaces" />
            <ref role="22LnvQ" node="6ULE2PD7rOv" resolve="statusCode" />
          </node>
        </node>
      </node>
      <node concept="2iuMTS" id="6ULE2PD7rHr" role="07xaq">
        <property role="TrG5h" value="createCollages" />
        <node concept="22YXZ_" id="6ULE2PD7rHt" role="22LnqS">
          <node concept="22YXW5" id="6ULE2PD7rHz" role="22YXZ$">
            <property role="TrG5h" value="iterator" />
            <node concept="0Z6TF" id="6ULE2PD7rHP" role="02Hm3">
              <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
              <ref role="3uLpB4" node="6ULE2PD7ryS" resolve="emotions" />
            </node>
          </node>
        </node>
        <node concept="3j0p_J" id="6ULE2PD7rHv" role="22LnvT">
          <node concept="07xbZ" id="6ULE2PD7rHW" role="07xaq">
            <property role="TrG5h" value="createCollage" />
            <node concept="07xbF" id="6ULE2PD7rHX" role="07xbH">
              <property role="TrG5h" value="Collage" />
            </node>
            <node concept="22YXZ_" id="6ULE2PD7rHY" role="3uUYZ6">
              <node concept="22YXW5" id="6ULE2PD7rI0" role="22YXZ$">
                <property role="TrG5h" value="bucket" />
                <node concept="0Z6TF" id="6ULE2PD7rIh" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7rv7" resolve="ds_project" />
                  <ref role="3uLpB4" node="6ULE2PD7rw0" resolve="bucket" />
                </node>
              </node>
              <node concept="22YXW5" id="6ULE2PD7rIk" role="22YXZ$">
                <property role="TrG5h" value="emotion" />
                <node concept="0Z6TF" id="6ULE2PD7rIO" role="02Hm3">
                  <ref role="0Z6TC" node="6ULE2PD7rHr" resolve="createCollages" />
                  <ref role="3uLpB4" node="6ULE2PD7rHz" resolve="iterator" />
                </node>
              </node>
            </node>
            <node concept="02HnI" id="6ULE2PD7rHZ" role="3uUYZp">
              <node concept="02HnH" id="6ULE2PD7rOY" role="02HnJ">
                <property role="TrG5h" value="statusCode" />
                <node concept="0eRJn" id="6ULE2PD7rP1" role="02Hm0" />
              </node>
            </node>
          </node>
        </node>
        <node concept="22LnvY" id="6ULE2PD7rHx" role="22LnvV">
          <node concept="22LnvN" id="6ULE2PD7rP5" role="22LnvL">
            <property role="TrG5h" value="statusCode" />
            <ref role="22LnvO" node="6ULE2PD7rHW" resolve="createCollage" />
            <ref role="22LnvQ" node="6ULE2PD7rOY" resolve="statusCode" />
          </node>
        </node>
      </node>
    </node>
    <node concept="3j0p_x" id="6ULE2PD7rv9" role="07xbz">
      <node concept="3j0p_I" id="6ULE2PD7rw0" role="3j0vfE">
        <property role="TrG5h" value="bucket" />
        <node concept="3xfQfl" id="6ULE2PD7rwq" role="02Hm3">
          <property role="3xcwG6" value="bucket" />
        </node>
        <node concept="0eRJm" id="6ULE2PD7rxx" role="02Hm0" />
      </node>
      <node concept="3j0p_I" id="6ULE2PD7rxN" role="3j0vfE">
        <property role="TrG5h" value="batch_size" />
        <node concept="0eRJn" id="6ULE2PD7ryc" role="02Hm0" />
        <node concept="3xfQfl" id="6ULE2PD7ryz" role="02Hm3">
          <property role="3xcwG6" value="batch_size" />
        </node>
      </node>
      <node concept="3j0p_I" id="6ULE2PD7ryS" role="3j0vfE">
        <property role="TrG5h" value="emotions" />
        <node concept="2imxK$" id="6ULE2PD7rz1" role="02Hm0" />
        <node concept="3xfQfl" id="6ULE2PD7rzs" role="02Hm3">
          <property role="3xcwG6" value="emotions" />
        </node>
      </node>
      <node concept="3j0p_I" id="6ULE2PD7rz_" role="3j0vfE">
        <property role="TrG5h" value="face_size" />
        <node concept="2imxK$" id="6ULE2PD7rzI" role="02Hm0" />
        <node concept="3xfQfl" id="6ULE2PD7r$5" role="02Hm3">
          <property role="3xcwG6" value="face_size" />
        </node>
      </node>
    </node>
    <node concept="3u$n2R" id="6ULE2PD7rva" role="07xbA">
      <node concept="3uzRnB" id="6ULE2PD7rPu" role="3u$n28">
        <property role="TrG5h" value="statusCode" />
        <ref role="3uzRnA" node="6ULE2PD7rHr" resolve="createCollages" />
        <ref role="3uzRnT" node="6ULE2PD7rP5" resolve="statusCode" />
      </node>
    </node>
  </node>
</model>

