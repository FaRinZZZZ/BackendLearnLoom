#!/usr/bin/python
# -*- coding: UTF-8 -*-
from openai import OpenAI
import os
import requests
import json
from dotenv import load_dotenv, dotenv_values
load_dotenv() 

def getNodeFromPDF(pdf):
    endpoint = 'https://api.opentyphoon.ai/v1/chat/completions'
    res = requests.post(endpoint, json={
        "model": "typhoon-v1.5x-70b-instruct",
        "max_tokens": 4000,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. You must answer only in Thai."
            },
            {
                
                "role": "user",
                "content": "สวัสดีครับ ผมเป็นนักเรียนหมอที่ต้องการเชื่อมโยงเรื่องราวดังต่อไปนี้ โดยต้องการที่จะอ่านแบบเร่งด่วนเลยนำสไลด์ที่ได้จากอาจารย์มาให้และช่วยสรุปเป็นหัวข้อว่าหัวข้อไหนเชื่อมกับอันไหนหน่อยครับให้ตอบออกมาในรูปแบบเป็น set และ subset โดยทุกหัวข้อ set ต้องขึ้นต้นด้วยคำว่า set และทุกหัวข้อ subsets ต้องขึ้นต้นด้วยคำว่า subsets​ และกำกับตัวเลขด้วยเท่านั้น และต้องไม่ตอบเป็น Question ด้วย ซึ่งหัวข้อย่อยสามารถมีหัวข้อย่อยของตัวมันเองอีกได้ " + pdf,
            }
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.05,
        "strem": False
    }, headers={
        "Authorization": "Bearer " + os.getenv("API_KEY"),
    })
    msg = json.loads(res.text)
    msg = msg["choices"][0]["message"]["content"]
    print(msg)
    print()
    node = {}
    key = "none"
    valid = False
    mode = 0
    for i in msg.split("\n"):
        sp = i.strip().split(" ")
        if(sp[0] != ""):
            print(sp)
            try:
                if(sp[0] == "Set"):
                    key = " ".join(sp[2:])
                    mode = 1
                elif(sp[0] == "Subsets:"):
                    mode = 2
                else:
                    valid = True
                    topic = " ".join(sp[1:])
                    topic = topic.split("(")[0]
                    if key in node.keys():
                        node[key].append(topic)
                    else:
                        node[key] = [topic]
                # if(sp[0] == "-" and (sp[1] == "Subset" or sp[1] == "Subsets")):
                #     valid = True
                #     topic = " ".join(sp[3:])
                #     topic = topic.split("(")[0]
                #     if key in node.keys():
                #         node[key].append(topic)
                #     else:
                #         node[key] = [topic]
            except:
                continue
    if(valid): print(node)
    else:
        print("Invalid response from Typhoon")
        return {"Message": "Invalid response from Typhoon"}
    return node

def getFlashCard(topic):
    endpoint = 'https://api.opentyphoon.ai/v1/chat/completions'
    res = requests.post(endpoint, json={
        "model": "typhoon-v1.5x-70b-instruct",
        "max_tokens": 4000,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. You must answer only in Thai."
            },
            {
                
                "role": "user",
                "content": "ให้สร้าง flash card เกี่ยวกับเนื้อหาเรื่องที่มีความเกี่ยวข้องกับ "+topic+"​ ในระดับค่อนข้างยาก จำนวน 8 ข้อ เป็นภาษาไทย โดยคำถามต้องมีข้อมูลมากพอสำหรับกาารหาคำตอบ และคำตอบต้องไม่เกิน2บรรทัด​ โดยมีรูปแบบเป็น question: และ answer:",
            }
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.05,
        "strem": False
    }, headers={
        "Authorization": "Bearer " + os.getenv("API_KEY"),
    })
    msg = json.loads(res.text)
    msg = msg["choices"][0]["message"]["content"]
    print(msg)
    print()
    flashCards = []
    valid = False
    for i in msg.split("\n"):
        sp = i.strip().split(" ")
        if(sp[0] != ""):
            print(sp)
            try:
                if(sp[1] == "Question:"):
                    flashCards.append({"Q": " ".join(sp[2:])})
                elif(sp[0] == "Answer:"):
                    valid = True
                    flashCards[-1]["A"] = " ".join(sp[1:])
            except:
                continue
    if(valid): print(flashCards)
    else:
        print("Invalid response from Typhoon")
        return {"Message": "Invalid response from Typhoon"}
    return flashCards

def getAiSummary(topic):
    endpoint = 'https://api.opentyphoon.ai/v1/chat/completions'
    res = requests.post(endpoint, json={
        "model": "typhoon-v1.5x-70b-instruct",
        "max_tokens": 4000,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. You must answer only in Thai."
            },
            {
                
                "role": "user",
                "content": "ทำการสรุปหัวข้อ "+topic+"ด้วยเนื้อหาระดับ นักศึกษาแพทย์มหาวิทยาลัย โดยมีเนื้อหากระชับและเข้าใจง่าย ไม่เกิน 4 บรรทัด และเป็น bullet point เป็นภาษาไทย"
            }
        ],
        "temperature": 0.3,
        "top_p": 0.9,
        "top_k": 50,
        "repetition_penalty": 1.05,
        "strem": False
    }, headers={
        "Authorization": "Bearer " + os.getenv("API_KEY"),
    })
    msg = json.loads(res.text)
    msg = msg["choices"][0]["message"]["content"]
    print(msg)
    return {"summary": msg}

if __name__ == "__main__":
    getNodeFromPDF('1.ผู้ป่ วยอายุ 18 กินยา choloquine และ primaquine แล้วมีปัสสาวะสีด า สาเหตุของการ เกิดอาการดังกล่าวเกิดจากการขาด enzyme ใด A. Phosphokinase B. Phospho-fructo-kinase C. Glutathione reductase D. Glucose-6-phosphate dehydrogenase E. Pentose-6-phosphate dehydrogenase 2. ชายอายุ 25 ปี เป็ น hemophilia A แต่งงานกับหญิง ที่เป็ นพาหะของ hemophilia บุตรที่เกิดมาจะมี โอกาสเป็ น hemophilia ร้อยละเท่าใด A. 25 B. 33 C. 50 D. 75 E. 100 3. ทารกแรกเกิด ซีด บวมน ้า ตับม้ามโต ขณะใกล้คลอดมารดามี ภาวะครรภ์เป็ นพิษ เด็กเสียชีวิตหลังคลอด 2 ชั่วโมง ตรวจ VDRL ให้ผลลบ Hemoglobin typing จะพบ A. Alpha 4 B. Beta 4 C. Gamma 4 D. Alpha2 gamma2 E. Beta2 gamma2 4. ชาย 30 ปี เมื่อ smear เลือดพบ normochromic normocytic, target cell, howell jolly bodies อยากทราบเข้ากับภาวะใด A. G6PD deficiency B. Thalassemia C. Post-spleenectomy D. Iron deficiency E. Megaloblastic anemia 5. เด็กชายอายุ 10 ปี มี echymosis ที่ขาซ้ายและขวา การตรวจ CBC พบว่า WBC, Hb, Hct ปกติ Platelet adequate ท่านจะส่ง LAB ใด เพิ่มเติม A. Prothrombin time B. Activated prothromboplastic time C. Bleeding time D. Venous clotting time E. Fibrinolysis time 6. ชายอายุ 50 ป ี มีอาการซีด เหนื่อยง่าย Hct 23%, WBC 3,200 cells/cu.mm. Platelet count 150,000 /cu.mm. จงให้การวินิจฉัย A. Hypersplenism B. Alplastic anemia C. Iron deficiency anemia D. Megaloblastic anemia E. Idiopathic thrombocytic purpura 7. ชาย 60 ป ี ซีด อ่อนเพลีย ปวดหลังมา 1 เดือน ตรวจ ร่างกายพบซีดปานกลางไม่เหลืองไม่พบการโตของ ตับ ม้ามและต่อมน ้าเหลือง Hb 8 Hct 24% WBC 6000 cells/cu.mm. N 65% L 35% Plt 200,000 /cu.mm. MCV 90 reticulocyte 1% blood smear พบ rouleaux formation พยาธิสภาพเกิด จากความผิดปกติของ cell กลุ่มใด A. monocyte B. Neutrophil C. Myeloblast D. Plasma cell E. Lymphocyte 8. เด็กชายอายุ 5 ป ี หกล้มหลังจากนั้น 3 ชั่วโมงมีอาการข้อ เข่าบวม จึงส่งตรวจ coagulogram ควรจะใช้ anticoagulant ใด ในการเจาะเลือดส่งตรวจ A. heparin B. Sodium citrate C. EDTA D. Sodium oxalate E. Sodium fluoride 9. หญิง 28 ป ี ก่อนการตั้งครรภ์ พบว่ามีอาการซีด Hb12 Hct 36% MCV 60 WBC และ PLT ปกติ Hv typing พบ A2 45% โครงสร้างใด ผิดปกติ A. Alpha B. Beta C. Gamma D. Delta E. Epsilon 10. หญิง 40 ป ี มีอาการเหนื่อยง่าย มีจุดเลือดออก ตรวจ ร่างกายพบว่า ซีด คล า ไม่พบตับม้ามและต่อมน ้าเหลือง โต CBC: Hb 7 WBC 3,500 (N 30, L 70) , platelet 30,000 MCV 92 จง ให้การวินิจฉัย A. hypersplenism B. Aplastic anemia C. Irondeficiency anemia D. Idiopathic thrombocytic purpura E. Sideroblastic anemia 11. ชาย 25 ป ี เป ็ นแผลในกระเพาะอาหาร ถ่ายอุจจาระด ามา 3 วัน CBC: Hb 10 WBC 7,000 Plt 300,000 reticulocyte 7% MCV 92 จงให้การวินิจฉัย A. Iron deficiency B. Pernicious anemia C. Hemolytic anemia D. Hepatoglobinopathy E. Post hemorrhagic anemia 12. ชายไทยอายุ 50 ปี มีอาการตัวเหลือง ตาเหลือง แบบ เป็ นๆหายๆ มี Hct ลด Hb ลด reticulocyte 12%, polychromasia, microspherocyte จากผลดังกล่าวเกิดจาก ความผิดปกติอะไร A. ขาด B12 B. ความผิดปกติของ Hb C. ภาวะพร่อง enzyme ของ RBC D. ผนังของ RBC ผิดปกติ E. Ab ต่อ RBC 13. ชายอายุ 18 ป ี ได้รับการตรวจการแข็งตัวของเลือดก่อน เข้ารับการผ่าตัด ผล coagulogram มีดังนี้ PTT 55 วินาที PT 12 วินาที ผลที่ผิดปกตินี้ เกิดจากขาด factor ใด A. Factor I B. Factor II C. Factor VII D. Factor VIII E. Factor X 14. หญิง 20 ปี ซีดเหลือง เป็ นๆหายๆ เป็ นมากเวลามีไข้ ม้ามโต คล าได้ต ่ากว่า 2 cm จาก right costal margin CBC: Hb 10, WBC 5,000 Plt 250,000 polychromasia microspherocyte จ านวนมาก coomb test negative สาเหตุ ของอาการป่ วยของผู้ป่ วยในข้อใด A. Ab ต่อ RBC B. มีความผิดปกติของ globin chain C. มีความผิดปกติของผนัง RBC D. ภาวะพร่อง enz ใน RBC E. ภาวะขาดเหล็ก 15. ผู้ป่ วยมี PTT 40 sec PT 40 sec ควรให้ สารใดเพิ่มเติม A. Vit A B. Vit B C. Vit C D. Vit D E. Vit /k 16.เด็กอายุ 6 ป ี มีจ ้าเลือดออกที่ superficial ecchymosis CBC: Hb 12 WBC 5,000 N 63% L20% E 12% M 5% Giant platelet pale 250,000 การทดสอบ LAB ให้ผงผิดปกติ A. Bleeding time B. Venous clotting time C. Clot retraction time D. Prothrombin time E. Thrombin time 17. คนไข้มีอาการซีด ตัวบวม มีภาวะไตวายเรื้อรัง Hct 24% Hb 8% WBC 6,000 Plt 200,000 MCV 80 ft. reticulocyte 0.1 % ผู้ป ่ วยรายนี้ขาดสารอะไร A. Vit B12 B. Erythropoietin C. Folic acid D. Colony stimulating factor E. Interleukin3 18. เด็ก 5 ปี ตัวซีด ตับม้ามโต peripheral blood smear พบ target few, schiztocytes few, hypochromic RBC 1+ ผู้ป่ วย น่าจะเป ็ นโรคใด A. Thalassemia B. G6PD deficiency C. Autoimmune hemolytic anemia D. Paroxysmal nocturnal hemolysis (PNH) E. Iron deficiency anemia 19. ผู้ป่ วยที่เป็ น G6PD deficiency จะตรวจพบ Heinz body ซึ่งเป็ น A. Remnant of nucleus B. Precipitated hemoglobin C. Hemosiderin granule D. Precipitated ribosome E. Aggregation of endoplasmic reticulum 20. ชายไทยอายุ 29 ป ี ถูกไฟไหม้ทั่วตัว มีจุดเลือดออกทั่ว ตัว aPTT prolong, PT prolong, จะ ตรวจ LAB อะไรเพื่อยืนยันอาการแทรกซ้อน ดังกล่าว A. Liver function test B. Venous clotting time C. Renal function test D. CBC E. Platelet count 21. ผู้ป ่ วยชายถ่ายอุจจาระเป ็ นมูกเลือด มีไข้ ตรวจ อุจจาระพบ RBC, WBC จ านวนมาก เชื้อที่เป ็ นสาเหตุของ การปวดเบ่งคือ A. Isospora belli B. Giardia lambria C. Entamoeba coli D. Entamoeba histolytica E. Cryptosporidium parvum 22.เก็กอายุ 10 ป ี คันง่ามนิ้วมือ ง่ามเท้า ขูดผิวหนังที่ง่ามนิ้ว มือมาย้อม KOH พบดังรูป • Phithiasis • Pediculosis • Scabiasis • Larva migran • Superficial eruption 23. หญิงอายุ 30 ปี เป็ น nephrotic syndrome ได้รับยา prednisolone มีผลต่อ WBC อย่างไร ผล LAB : WBC 14,000 Plt 200,000 (neutrophil สูง, Lymphocyte ต ่า) A. กระตุ้น bonemarrow สร้าง B. Neutrophil ถูกท าลายน้อยลง C. เร่ง maturation ของ neutrophil D. เพิ่ม permeability/ กระตุ้น migrate จาก ผนัง vessel ไปสู่ circulation E. กระตุ้น granulocyte CSF 24. ทารกตายคลอดเป็ นแบบ hydrop fetalis ตรวจ cord blood พบ Hb Bart ทารกนี้มี genotype แบบใด A. beta-thal 0/ beta-thal 0 B. Beta-thal1/beta-thal1 C. Alpha-thal1/alpha-thal1 D. Alpha-thal1/alpha-thal2 E. Alpha-thal2/alpha-thal2 25. เด็ก 10 ปี มีไข้ ซึม มีอาการ stiffneck ตรวจ CSF พบ WBC 1200 N=90% L=10% sugar 20 (blood sugar 100) protein สูง จงให้การวินิจฉัยว่าติดเชื้อใด A. Entero virus B. N. fowleri C. N. meningitidis D. Toxoplasma gondii E. Cryptococcus neoformans 26. ผู้ป ่ วยหญิงเป ็ นมะเร็งล าไส้ หลังผ่าตัดเอาเนื้องอกออก marker ใด สามารถติดตามการกลบมาของโรคได้ A. CEA B. Alpha-fetoprotein C. ALP D. ALT E. CA-125')
    #getFlashCard('Disseminated intravascular coagulation', 5)
    #getAiSummary('Disseminated intravascular coagulation')