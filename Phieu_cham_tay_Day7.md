# Phiếu chấm tay Day 7 — tài liệu để TỰ đọc và TỰ đánh giá

Câu hỏi và đáp án benchmark có AI hỗ trợ soạn bản nháp. Người học đã tự đối chiếu PDF và ghi xác nhận trong phiếu; các điểm review agent được lưu riêng trong `results/agent/review-test-baseline/` và `results/agent/review-test-selected/`.

## Thang điểm (theo RUBRIC/BENCHMARK của đề)

| Chỉ số | Cách chấm |
|---|---|
| Context (0/1/2) | 0 = context không chứa evidence · 1 = có evidence nhưng thiếu điều kiện hoặc nguồn · 2 = đủ |
| Answer (0/1/2) | 0 = sai hoặc thiếu evidence (từ chối câu có đáp án = 0) · 1 = đúng một phần · 2 = đúng và đủ |
| Citation | Mỗi citation: đoạn được trích có **thực sự hỗ trợ** câu trả lời không (true/false). ID hợp lệ chưa đủ |
| Câu thiếu evidence | Agent từ chối và không thêm khẳng định vô căn cứ; bạn tự xác nhận tài liệu thật sự không trả lời |

Quy trình gợi ý cho mỗi câu: (1) đọc câu hỏi, (2) đọc đoạn gốc, (3) đọc context agent thấy, (4) đọc câu trả lời, (5) đọc từng đoạn được trích, (6) mới chấm.


---
# PHẦN A. Xác nhận 5 câu test có đáp án (bản nháp có AI hỗ trợ soạn)

Với mỗi câu, tự kiểm tra: đáp án mong đợi có đúng với đoạn gốc không? Câu hỏi có hiểu được độc lập không? Có chép nguyên văn từ tài liệu không?

## q21

**Câu hỏi:** Within Part 1, when measuring impacts across a population, what should analysts keep in mind about which groups may be affected and their relationship to the system?

**Đáp án mong đợi (trong benchmark):** Because harms can affect groups differently, and potentially harmed communities may not be direct system users.

**Loại:** paraphrase · **Bộ lọc dự kiến:** {'part': 'part1'}

**Đoạn gốc** `nist-ai-100-1-para-p011-c01` (trang PDF 11):

> Approaches for measuring impacts on a population work best if they recognize that contexts matter, that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system.

Bạn xác nhận: ☒ đáp án đúng với đoạn gốc   ☒ câu hỏi rõ ràng   ☒ không chép nguyên văn   Ghi chú: Đối chiếu PDF trang 11: câu gốc khớp đáp án; câu hỏi nêu rõ Part 1 nên hiểu độc lập; đáp án là diễn đạt lại, không chép nguyên văn.


## q22

**Câu hỏi:** How does the AI RMF define an organization's risk tolerance?

**Đáp án mong đợi (trong benchmark):** Its readiness to bear risk in order to achieve its objectives.

**Loại:** paraphrase · **Bộ lọc dự kiến:** None

**Đoạn gốc** `nist-ai-100-1-para-p012-c00` (trang PDF 12):

> 1.2.2 Risk Tolerance While the AI RMF can be used to prioritize risk, it does not prescribe risk tolerance. Risk tolerance refers to the organization’s or AI actor’s (see Appendix A) readiness to bear the risk in order to achieve its objectives. Risk tolerance can be influenced by legal or regulatory requirements (Adapted from: ISO GUIDE 73). Risk tolerance and the level of risk that is acceptable to organizations or society are highly contextual and application and use-case specific. Risk tolerances can be influenced by policies and norms established by AI system owners, organizations, industries, communities, or policy makers. Risk tolerances are likely to change over time as AI systems, policies, and norms evolve. Different organizations may have varied risk tolerances due to their

Bạn xác nhận: ☒ đáp án đúng với đoạn gốc   ☒ câu hỏi rõ ràng   ☒ không chép nguyên văn   Ghi chú: Đối chiếu PDF trang 12: câu định nghĩa khớp đáp án. Chunk bị cắt sau “due to their” nhưng định nghĩa vẫn đủ; đáp án là diễn đạt lại.


## q23

**Câu hỏi:** Must an organization follow the four AI RMF functions in one fixed sequence?

**Đáp án mong đợi (trong benchmark):** No. They may be performed in any order that adds value, and the process should be iterative.

**Loại:** paraphrase · **Bộ lọc dự kiến:** None

**Đoạn gốc** `nist-ai-100-1-para-p026-c01` (trang PDF 26):

> Framework users may apply these functions as best suits their needs for managing AI risks based on their resources and capabilities. Some organizations may choose to select from among the categories and subcategories; others may choose and have the capacity to apply all categories and subcategories. Assuming a governance structure is in place, functions may be performed in any order across the AI lifecycle as deemed to add value by a user of the framework. After instituting the outcomes in GOVERN, most users of the AI RMF would start with the MAP function and continue to MEASURE or MANAGE. However users integrate the functions, the process should be iterative, with cross-referencing between functions as necessary. Similarly, there are categories and subcategories with elements that

Bạn xác nhận: ☒ đáp án đúng với đoạn gốc   ☒ câu hỏi rõ ràng   ☒ không chép nguyên văn   Ghi chú: Đối chiếu PDF trang 26: “any order… iterative” khớp đáp án. Đáp án bỏ ý “most users would start with MAP” nhưng không làm sai câu trả lời.


## q24

**Câu hỏi:** Who can set the policies that direct an organization's mission, values, culture, and risk tolerance?

**Đáp án mong đợi (trong benchmark):** Governing authorities.

**Loại:** paraphrase · **Bộ lọc dự kiến:** None

**Đoạn gốc** `nist-ai-100-1-para-p027-c01` (trang PDF 27):

> Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.

Bạn xác nhận: ☒ đáp án đúng với đoạn gốc   ☒ câu hỏi rõ ràng   ☒ không chép nguyên văn   Ghi chú: Đối chiếu PDF trang 27: governing authorities khớp đáp án; câu hỏi rõ; đáp án ngắn, không chép nguyên văn.


## q25

**Câu hỏi:** For the MAP 1.2 team described in Part 2, what kinds of diversity and experience should be reflected in participants?

**Đáp án mong đợi (trong benchmark):** Demographic diversity and broad domain and user experience expertise.

**Loại:** paraphrase · **Bộ lọc dự kiến:** {'part': 'part2'}

**Đoạn gốc** `nist-ai-100-1-para-p031-c01` (trang PDF 31):

> MAP 1.2: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized. MAP 1.3: The organization’s mission and relevant goals for AI technology are understood and documented. MAP 1.4: The business value or context of business use has been clearly defined or – in the case of assessing existing AI systems – re-evaluated. MAP 1.5: Organizational risk tolerances are determined and documented.

Bạn xác nhận: ☒ đáp án đúng với đoạn gốc   ☒ câu hỏi rõ ràng   ☒ không chép nguyên văn   Ghi chú: Đối chiếu PDF trang 31: MAP 1.2 khớp đáp án; câu hỏi nêu rõ Part 2 và MAP 1.2; đáp án là diễn đạt lại.


---
# PHẦN B. Xác nhận 4 câu thiếu evidence (dev 2 + test 2)

Việc bạn cần làm: mở PDF, tìm từ khóa, và đọc phần gần chủ đề để tự kết luận tài liệu có trả lời được hay không. Dưới đây là số lần từ khóa xuất hiện trong 175 chunk (do chương trình đếm, **chưa phải kết luận**) và 3 đoạn gần chủ đề nhất theo BM25 để bạn đọc.


## u-dev-01 (dev)

**Câu hỏi:** Which GDPR articles does the AI RMF map its privacy subcategories to?

**Lý do thiếu đã ghi trong benchmark:** Đã tìm GDPR trên toàn bộ 42 trang nội dung (0 lần); phần Privacy (PDF page 22) bàn về nguyên tắc và rủi ro quyền riêng tư, không nêu điều khoản GDPR.

**Số lần xuất hiện của từ khóa (máy đếm):** `gdpr` = 0, `general data protection` = 0, `article` = 0

**3 đoạn gần chủ đề nhất (để bạn đọc):**

- `nist-ai-100-1-para-p008-c00` (trang 8): valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy enhanced, and fair with their harmful biases managed. Part 2 comprises the “Core” of the Framework. It describes four specific functions to help organizations address the risks of AI systems in practice. These functions – GOVERN, MAP, MEASURE, and MANAGE – are broken down further into categories and subcategories. While GOVERN applies to all stages of organizations’ AI risk management processes and procedures, the MAP, MEASURE, and MANAGE functions can be applied in AI system-specific contexts and at specific stages of the AI lifecycle. Additional resources related to the Framework are included in the AI RMF Playbook, which is available via the NIST AI RMF website:

- `nist-ai-100-1-para-p044-c02` (trang 44): Framework. These frameworks have some features in common with the AI RMF. Like most risk management approaches, they are outcome-based rather than prescriptive and are often structured around a Core set of functions, categories, and subcategories. While there are significant differences between these frameworks based on the domain addressed – and because AI risk management calls for addressing many other types of risks – frameworks like those mentioned above may inform security and privacy considerations in the MAP, MEASURE, and MANAGE functions of the AI RMF. At the same time, guidance available before publication of this AI RMF does not comprehensively address many AI system risks. For example, existing frameworks and guidance are unable to:

- `nist-ai-100-1-para-p025-c00` (trang 25): Part 2: Core and Profiles 5. AI RMF Core The AI RMF Core provides outcomes and actions that enable dialogue, understanding, and activities to manage AI risks and responsibly develop trustworthy AI systems. As illustrated in Figure 5, the Core is composed of four functions: GOVERN, MAP, MEASURE, and MANAGE. Each of these high-level functions is broken down into categories and subcategories. Categories and subcategories are subdivided into specific actions and outcomes. Actions do not constitute a checklist, nor are they necessarily an ordered set of steps.

Kết luận của bạn sau khi đọc PDF: ☒ tài liệu không trả lời được   ☐ tài liệu có trả lời (câu này phải sửa)   Đã đọc phần/trang: trang 8, 22, 25, 44   Ghi chú: Đọc trang 8, 22, 25, 44 (mục Privacy-Enhanced ở trang 22). Tìm toàn PDF: GDPR, General Data Protection, Article đều 0 lần.


## u-dev-02 (dev)

**Câu hỏi:** Which differential privacy algorithm does the AI RMF recommend for protecting training data?

**Lý do thiếu đã ghi trong benchmark:** Đã tìm cụm differential privacy trên toàn bộ 42 trang nội dung (0 lần); tài liệu nói về privacy-enhancing techniques nhưng không chỉ định thuật toán differential privacy.

**Số lần xuất hiện của từ khóa (máy đếm):** `differential privacy` = 0, `privacy-enhancing` = 2, `algorithm` = 4

**3 đoạn gần chủ đề nhất (để bạn đọc):**

- `nist-ai-100-1-para-p013-c04` (trang 13): The AI RMF may be utilized along with related guidance and frameworks for managing AI system risks or broader enterprise risks. Some risks related to AI systems are common across other types of software development and deployment. Examples of overlapping risks include: privacy concerns related to the use of underlying data to train AI systems; the energy and environmental implications associated with resource-heavy computing demands; security concerns related to the confidentiality, integrity, and availability of the system and its training and output data; and general security of the underlying software and hardware for AI systems.

- `nist-ai-100-1-para-p040-c02` (trang 40): 2. AI Development actors provide the initial infrastructure of AI systems and are responsible for model building and interpretation tasks, which involve the creation, selection, calibration, training, and/or testing of models or algorithms. AI actors in this category include machine learning experts, data scientists, developers, third-party entities, legal and privacy governance experts, and experts in the socio-cultural and contextual factors associated with the deployment setting.

- `nist-ai-100-1-para-p021-c02` (trang 21): Measures to enhance transparency and accountability should also consider the impact of these efforts on the implementing entity, including the level of necessary resources and the need to safeguard proprietary information. Maintaining the provenance of training data and supporting attribution of the AI system’s decisions to subsets of training data can assist with both transparency and accountability. Training data may also be subject to copyright and should follow applicable intellectual property rights laws. As transparency tools for AI systems and related documentation continue to evolve, developers of AI systems are encouraged to test different types of transparency tools in cooperation with AI deployers to ensure that AI systems are used as intended.

Kết luận của bạn sau khi đọc PDF: ☒ tài liệu không trả lời được   ☐ tài liệu có trả lời (câu này phải sửa)   Đã đọc phần/trang: trang 13, 17, 21, 22, 40   Ghi chú: Đọc trang 13, 21, 22, 40. Tìm toàn PDF: differential privacy 0 lần; privacy-enhancing xuất hiện ở trang 17 và 22 nhưng không nêu thuật toán.


## u-test-01 (test)

**Câu hỏi:** How many hours of red-team testing does the framework require before an AI system is released?

**Lý do thiếu đã ghi trong benchmark:** Đã tìm red team/red-team trên toàn bộ 42 trang nội dung (0 lần); tài liệu không đặt số giờ thử nghiệm bắt buộc.

**Số lần xuất hiện của từ khóa (máy đếm):** `red team` = 0, `red-team` = 0, `red teaming` = 0, `hours` = 0

**3 đoạn gần chủ đề nhất (để bạn đọc):**

- `nist-ai-100-1-para-p044-c02` (trang 44): Framework. These frameworks have some features in common with the AI RMF. Like most risk management approaches, they are outcome-based rather than prescriptive and are often structured around a Core set of functions, categories, and subcategories. While there are significant differences between these frameworks based on the domain addressed – and because AI risk management calls for addressing many other types of risks – frameworks like those mentioned above may inform security and privacy considerations in the MAP, MEASURE, and MANAGE functions of the AI RMF. At the same time, guidance available before publication of this AI RMF does not comprehensively address many AI system risks. For example, existing frameworks and guidance are unable to:

- `nist-ai-100-1-para-p043-c02` (trang 43): • AI system scale and complexity (many systems contain billions or even trillions of decision points) housed within more traditional software applications. • Use of pre-trained models that can advance research and improve performance can also increase levels of statistical uncertainty and cause issues with bias management, scientific validity, and reproducibility. • Higher degree of difficulty in predicting failure modes for emergent properties of large-scale pre-trained models. • Privacy risk due to enhanced data aggregation capability for AI systems. • AI systems may require more frequent maintenance and triggers for conducting corrective maintenance due to data, model, or concept drift. • Increased opacity and concerns about reproducibility.

- `nist-ai-100-1-para-p007-c02` (trang 7): As directed by the National Artificial Intelligence Initiative Act of 2020 (P.L. 116-283), the goal of the AI RMF is to offer a resource to the organizations designing, developing, deploying, or using AI systems to help manage the many risks of AI and promote trustworthy and responsible development and use of AI systems. The Framework is intended to be voluntary, rights-preserving, non-sector-specific, and use-case agnostic, providing flexibility to organizations of all sizes and in all sectors and throughout society to implement the approaches in the Framework.

Kết luận của bạn sau khi đọc PDF: ☒ tài liệu không trả lời được   ☐ tài liệu có trả lời (câu này phải sửa)   Đã đọc phần/trang: trang 7, 43, 44   Ghi chú: Đọc trang 7, 43, 44. Tìm toàn PDF: red team, red-teaming, hours đều 0 lần; framework tự nguyện, không đặt số giờ.


## u-test-02 (test)

**Câu hỏi:** Which federated learning protocol does the AI RMF recommend?

**Lý do thiếu đã ghi trong benchmark:** Đã tìm federated learning trên toàn bộ 42 trang nội dung (0 lần); AI RMF không nêu giao thức học liên kết cụ thể.

**Số lần xuất hiện của từ khóa (máy đếm):** `federated` = 0, `federated learning` = 0, `protocol` = 1

**3 đoạn gần chủ đề nhất (để bạn đọc):**

- `nist-ai-100-1-para-p044-c03` (trang 44): • adequately manage the problem of harmful bias in AI systems; • confront the challenging risks related to generative AI; • comprehensively address security concerns related to evasion, model extraction, membership inference, availability, or other machine learning attacks; • account for the complex attack surface of AI systems or other security abuses enabled by AI systems; and • consider risks associated with third-party AI technologies, transfer learning, and offlabel use where AI systems may be trained for decision-making outside an organization’s security controls or trained in one domain and then “fine-tuned” for another. Both AI and traditional software technologies and systems are subject to rapid innovation.

- `nist-ai-100-1-para-p040-c02` (trang 40): 2. AI Development actors provide the initial infrastructure of AI systems and are responsible for model building and interpretation tasks, which involve the creation, selection, calibration, training, and/or testing of models or algorithms. AI actors in this category include machine learning experts, data scientists, developers, third-party entities, legal and privacy governance experts, and experts in the socio-cultural and contextual factors associated with the deployment setting.

- `nist-ai-100-1-para-p043-c00` (trang 43): Appendix B: How AI Risks Differ from Traditional Software Risks As with traditional software, risks from AI-based technology can be bigger than an enterprise, span organizations, and lead to societal impacts. AI systems also bring a set of risks that are not comprehensively addressed by current risk frameworks and approaches. Some AI system features that present risks also can be beneficial. For example, pre-trained models and transfer learning can advance research and increase accuracy and resilience when compared to other models and approaches. Identifying contextual factors in theMAP function will assist AI actors in determining the level of risk and potential management efforts. Compared to traditional software, AI-specific risks that are new or increased include the following:

Kết luận của bạn sau khi đọc PDF: ☒ tài liệu không trả lời được   ☐ tài liệu có trả lời (câu này phải sửa)   Đã đọc phần/trang: trang 40, 43, 44   Ghi chú: Đọc trang 40, 43, 44. Tìm toàn PDF: federated 0 lần (chỉ có “Federal” ở trang 8); không có giao thức nào được khuyến nghị.


---
# PHẦN C. Chấm câu trả lời của agent (7 câu × 2 cấu hình)


## q21 — câu có đáp án

**Câu hỏi:** Within Part 1, when measuring impacts across a population, what should analysts keep in mind about which groups may be affected and their relationship to the system?

**Đáp án mong đợi:** Because harms can affect groups differently, and potentially harmed communities may not be direct system users.

**Đoạn gốc** `nist-ai-100-1-para-p011-c01` (trang 11): > Approaches for measuring impacts on a population work best if they recognize that contexts matter, that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system.


### q21 · BASELINE (BM25, không filter)

- Trạng thái: **answered** · số lượt search: 1 · các query: ['Part 1 measuring impacts across a population groups affected relationship to the system']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(11, 'nist-ai-100-1-para-p011-c01'), (42, 'nist-ai-100-1-para-p042-c02'), (34, 'nist-ai-100-1-para-p034-c01')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p011-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: True

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p011-c01 | NIST.AI.100-1.pdf | page 11]
Approaches for measuring impacts on a population work best if they recognize that contexts matter, that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system.
```

**Câu trả lời của agent:** Analysts should keep in mind that contexts matter when measuring impacts across a population. They should recognize that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system [nist-ai-100-1-para-p011-c01].

**Citations:** ['nist-ai-100-1-para-p011-c01']

*Đoạn được trích `nist-ai-100-1-para-p011-c01` (trang 11):*
> Approaches for measuring impacts on a population work best if they recognize that contexts matter, that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system.

**Bạn chấm:**  Context = 2   Answer = 2   Citation support (từng citation: true/false) = true

**Lý do (tiếng Việt, lời của bạn):** Context chứa đúng câu gốc ở trang 11. Câu trả lời nêu đủ hai ý: tác hại có thể ảnh hưởng nhóm khác nhau và nhóm bị hại không nhất thiết là người dùng trực tiếp.


### q21 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **answered** · số lượt search: 1 · các query: ['Part 1 measuring impacts across a population groups affected relationship to the system']
- Bộ lọc đã áp dụng: {'part': 'part1'}
- Top-3 tìm được: [(11, 'nist-ai-100-1-para-p011-c01'), (9, 'nist-ai-100-1-para-p009-c00'), (22, 'nist-ai-100-1-para-p022-c04')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p011-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: True

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p011-c01 | NIST.AI.100-1.pdf | page 11]
Approaches for measuring impacts on a population work best if they recognize that contexts matter, that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system.
```

**Câu trả lời của agent:** Analysts should keep in mind that contexts matter when measuring impacts across a population. They should recognize that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system [nist-ai-100-1-para-p011-c01].

**Citations:** ['nist-ai-100-1-para-p011-c01']

*Đoạn được trích `nist-ai-100-1-para-p011-c01` (trang 11):*
> Approaches for measuring impacts on a population work best if they recognize that contexts matter, that harms may affect varied groups or sub-groups differently, and that communities or other sub-groups who may be harmed are not always direct users of a system.

**Bạn chấm:**  Context = 2   Answer = 2   Citation support (từng citation: true/false) = true

**Lý do (tiếng Việt, lời của bạn):** Context chứa đúng câu gốc ở trang 11 (bộ lọc part1 không đổi kết quả). Trả lời đủ hai ý, đúng với đoạn trích; citation p011-c01 hỗ trợ trực tiếp.


## q22 — câu có đáp án

**Câu hỏi:** How does the AI RMF define an organization's risk tolerance?

**Đáp án mong đợi:** Its readiness to bear risk in order to achieve its objectives.

**Đoạn gốc** `nist-ai-100-1-para-p012-c00` (trang 12): > 1.2.2 Risk Tolerance While the AI RMF can be used to prioritize risk, it does not prescribe risk tolerance. Risk tolerance refers to the organization’s or AI actor’s (see Appendix A) readiness to bear the risk in order to achieve its objectives. Risk tolerance can be influenced by legal or regulatory requirements (Adapted from: ISO GUIDE 73). Risk tolerance and the level of risk that is acceptable to organizations or society are highly contextual and application and use-case specific. Risk tolerances can be influenced by policies and norms established by AI system owners, organizations, industries, communities, or policy makers. Risk tolerances are likely to change over time as AI systems, policies, and norms evolve. Different organizations may have varied risk tolerances due to their


### q22 · BASELINE (BM25, không filter)

- Trạng thái: **abstain** · số lượt search: 2 · các query: ["AI RMF organization's risk tolerance definition", 'AI RMF risk tolerance definition']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(12, 'nist-ai-100-1-para-p012-c00'), (12, 'nist-ai-100-1-para-p012-c02'), (38, 'nist-ai-100-1-para-p038-c02')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p042-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: False

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p042-c01 | NIST.AI.100-1.pdf | page 42]
Additional AI Actors Third-party entities include providers, developers, vendors, and evaluators of data, algorithms, models, and/or systems and related services for another organization or the organization’s customers or clients. Third-party entities are responsible for AI design and development tasks, in whole or in part. By definition, they are external to the design, development, or deployment team of the organization that acquires its technologies or services. The technologies acquired from third-party entities may be complex or opaque, and risk tolerances may not align with the deploying or operating organization.
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Context = 0   Answer = 0   Citation support (từng citation: true/false) = không có citation

**Lý do (tiếng Việt, lời của bạn):** Chunk gốc p012-c00 đứng hạng 1 nhưng context chỉ có p042-c01 (nói về bên thứ ba), không chứa định nghĩa. Agent từ chối câu có đáp án nên Answer = 0.


### q22 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **answered** · số lượt search: 1 · các query: ["organization's risk tolerance AI RMF"]
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(12, 'nist-ai-100-1-para-p012-c00'), (27, 'nist-ai-100-1-para-p027-c01'), (27, 'nist-ai-100-1-para-p027-c03')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p027-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: False

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p027-c01 | NIST.AI.100-1.pdf | page 27]
Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.
```

**Câu trả lời của agent:** The AI RMF defines an organization's risk tolerance as determined by governing authorities who establish overarching policies that guide the organization's mission, goals, values, culture, and risk tolerance. Senior leadership plays a crucial role in setting the tone for risk management and shaping the organizational culture related to risk [nist-ai-100-1-para-p027-c01].

**Citations:** ['nist-ai-100-1-para-p027-c01']

*Đoạn được trích `nist-ai-100-1-para-p027-c01` (trang 27):*
> Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.

**Bạn chấm:**  Context = 0   Answer = 0   Citation support (từng citation: true/false) = false

**Lý do (tiếng Việt, lời của bạn):** Context chỉ có p027-c01, đoạn này nói cơ quan quản trị đặt chính sách chứ không định nghĩa risk tolerance. Agent trả lời sai là định nghĩa; định nghĩa đúng ở p012-c00 không vào context.


## q23 — câu có đáp án

**Câu hỏi:** Must an organization follow the four AI RMF functions in one fixed sequence?

**Đáp án mong đợi:** No. They may be performed in any order that adds value, and the process should be iterative.

**Đoạn gốc** `nist-ai-100-1-para-p026-c01` (trang 26): > Framework users may apply these functions as best suits their needs for managing AI risks based on their resources and capabilities. Some organizations may choose to select from among the categories and subcategories; others may choose and have the capacity to apply all categories and subcategories. Assuming a governance structure is in place, functions may be performed in any order across the AI lifecycle as deemed to add value by a user of the framework. After instituting the outcomes in GOVERN, most users of the AI RMF would start with the MAP function and continue to MEASURE or MANAGE. However users integrate the functions, the process should be iterative, with cross-referencing between functions as necessary. Similarly, there are categories and subcategories with elements that


### q23 · BASELINE (BM25, không filter)

- Trạng thái: **abstain** · số lượt search: 1 · các query: ['four AI RMF functions sequence']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(25, 'nist-ai-100-1-para-p025-c00'), (8, 'nist-ai-100-1-para-p008-c00'), (25, 'nist-ai-100-1-para-p025-c01')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p025-c00']
- (máy đo) chunk gốc có trong top-3: False · có trong context: False

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p025-c00 | NIST.AI.100-1.pdf | page 25]
Part 2: Core and Profiles 5. AI RMF Core The AI RMF Core provides outcomes and actions that enable dialogue, understanding, and activities to manage AI risks and responsibly develop trustworthy AI systems. As illustrated in Figure 5, the Core is composed of four functions: GOVERN, MAP, MEASURE, and MANAGE. Each of these high-level functions is broken down into categories and subcategories. Categories and subcategories are subdivided into specific actions and outcomes. Actions do not constitute a checklist, nor are they necessarily an ordered set of steps.
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Context = 0   Answer = 0   Citation support (từng citation: true/false) = không có citation

**Lý do (tiếng Việt, lời của bạn):** Context chỉ có p025-c00; câu 'không nhất thiết là một chuỗi có thứ tự' ở đó nói về actions, không phải bốn functions. Đoạn gốc p026-c01 không vào top-3. Từ chối câu có đáp án = 0.


### q23 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **abstain** · số lượt search: 1 · các query: ['four AI RMF functions sequence']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(25, 'nist-ai-100-1-para-p025-c00'), (8, 'nist-ai-100-1-para-p008-c00'), (25, 'nist-ai-100-1-para-p025-c01')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p025-c00']
- (máy đo) chunk gốc có trong top-3: False · có trong context: False

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p025-c00 | NIST.AI.100-1.pdf | page 25]
Part 2: Core and Profiles 5. AI RMF Core The AI RMF Core provides outcomes and actions that enable dialogue, understanding, and activities to manage AI risks and responsibly develop trustworthy AI systems. As illustrated in Figure 5, the Core is composed of four functions: GOVERN, MAP, MEASURE, and MANAGE. Each of these high-level functions is broken down into categories and subcategories. Categories and subcategories are subdivided into specific actions and outcomes. Actions do not constitute a checklist, nor are they necessarily an ordered set of steps.
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Context = 0   Answer = 0   Citation support (từng citation: true/false) = không có citation

**Lý do (tiếng Việt, lời của bạn):** Giống baseline: cùng query, cùng top-3, context chỉ có p025-c00 và thiếu p026-c01 (functions có thể thực hiện theo thứ tự bất kỳ, quá trình lặp). Từ chối câu có đáp án nên Answer = 0.


## q24 — câu có đáp án

**Câu hỏi:** Who can set the policies that direct an organization's mission, values, culture, and risk tolerance?

**Đáp án mong đợi:** Governing authorities.

**Đoạn gốc** `nist-ai-100-1-para-p027-c01` (trang 27): > Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.


### q24 · BASELINE (BM25, không filter)

- Trạng thái: **answered** · số lượt search: 1 · các query: ["who can set the policies that direct an organization's mission values culture risk tolerance"]
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(27, 'nist-ai-100-1-para-p027-c01'), (12, 'nist-ai-100-1-para-p012-c00'), (27, 'nist-ai-100-1-para-p027-c03')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p027-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: True

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p027-c01 | NIST.AI.100-1.pdf | page 27]
Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.
```

**Câu trả lời của agent:** Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Additionally, senior leadership sets the tone for risk management within the organization, influencing its culture [nist-ai-100-1-para-p027-c01].

**Citations:** ['nist-ai-100-1-para-p027-c01']

*Đoạn được trích `nist-ai-100-1-para-p027-c01` (trang 27):*
> Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.

**Bạn chấm:**  Context = 2   Answer = 2   Citation support (từng citation: true/false) = true

**Lý do (tiếng Việt, lời của bạn):** Context có đúng câu về governing authorities ở trang 27. Trả lời đúng đáp án; phần thêm về senior leadership có trong cùng đoạn nên không bịa.


### q24 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **answered** · số lượt search: 1 · các query: ["who sets policies for organization's mission values culture risk tolerance"]
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(27, 'nist-ai-100-1-para-p027-c01'), (12, 'nist-ai-100-1-para-p012-c00'), (27, 'nist-ai-100-1-para-p027-c03')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p027-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: True

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p027-c01 | NIST.AI.100-1.pdf | page 27]
Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.
```

**Câu trả lời của agent:** Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Additionally, senior leadership sets the tone for risk management within the organization, influencing its culture [nist-ai-100-1-para-p027-c01].

**Citations:** ['nist-ai-100-1-para-p027-c01']

*Đoạn được trích `nist-ai-100-1-para-p027-c01` (trang 27):*
> Strong governance can drive and enhance internal practices and norms to facilitate organizational risk culture. Governing authorities can determine the overarching policies that direct an organization’s mission, goals, values, culture, and risk tolerance. Senior leadership sets the tone for risk management within an organization, and with it, organizational culture. Management aligns the technical aspects of AI risk management to policies and operations. Documentation can enhance transparency, improve human review processes, and bolster accountability in AI system teams.

**Bạn chấm:**  Context = 2   Answer = 2   Citation support (từng citation: true/false) = true

**Lý do (tiếng Việt, lời của bạn):** Context có đúng câu về governing authorities ở trang 27. Trả lời đúng và đủ; câu thêm về senior leadership được chính đoạn trích hỗ trợ.


## q25 — câu có đáp án

**Câu hỏi:** For the MAP 1.2 team described in Part 2, what kinds of diversity and experience should be reflected in participants?

**Đáp án mong đợi:** Demographic diversity and broad domain and user experience expertise.

**Đoạn gốc** `nist-ai-100-1-para-p031-c01` (trang 31): > MAP 1.2: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized. MAP 1.3: The organization’s mission and relevant goals for AI technology are understood and documented. MAP 1.4: The business value or context of business use has been clearly defined or – in the case of assessing existing AI systems – re-evaluated. MAP 1.5: Organizational risk tolerances are determined and documented.


### q25 · BASELINE (BM25, không filter)

- Trạng thái: **answered** · số lượt search: 1 · các query: ['MAP 1.2 team diversity experience participants']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(31, 'nist-ai-100-1-para-p031-c01'), (28, 'nist-ai-100-1-para-p028-c02'), (14, 'nist-ai-100-1-para-p014-c01')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p031-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: True

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p031-c01 | NIST.AI.100-1.pdf | page 31]
MAP 1.2: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized. MAP 1.3: The organization’s mission and relevant goals for AI technology are understood and documented. MAP 1.4: The business value or context of business use has been clearly defined or – in the case of assessing existing AI systems – re-evaluated. MAP 1.5: Organizational risk tolerances are determined and documented.
```

**Câu trả lời của agent:** The MAP 1.2 team should reflect demographic diversity and broad domain and user experience expertise among its participants. Additionally, opportunities for interdisciplinary collaboration are prioritized [nist-ai-100-1-para-p031-c01].

**Citations:** ['nist-ai-100-1-para-p031-c01']

*Đoạn được trích `nist-ai-100-1-para-p031-c01` (trang 31):*
> MAP 1.2: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized. MAP 1.3: The organization’s mission and relevant goals for AI technology are understood and documented. MAP 1.4: The business value or context of business use has been clearly defined or – in the case of assessing existing AI systems – re-evaluated. MAP 1.5: Organizational risk tolerances are determined and documented.

**Bạn chấm:**  Context = 2   Answer = 2   Citation support (từng citation: true/false) = true

**Lý do (tiếng Việt, lời của bạn):** Context có nguyên MAP 1.2 ở trang 31. Trả lời đúng: đa dạng nhân khẩu học và chuyên môn rộng về lĩnh vực, trải nghiệm người dùng; ý hợp tác liên ngành cũng có trong đoạn.


### q25 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **answered** · số lượt search: 1 · các query: ['MAP 1.2 team diversity experience participants']
- Bộ lọc đã áp dụng: {'part': 'part2'}
- Top-3 tìm được: [(31, 'nist-ai-100-1-para-p031-c01'), (28, 'nist-ai-100-1-para-p028-c02'), (32, 'nist-ai-100-1-para-p032-c03')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p031-c01']
- (máy đo) chunk gốc có trong top-3: True · có trong context: True

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p031-c01 | NIST.AI.100-1.pdf | page 31]
MAP 1.2: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized. MAP 1.3: The organization’s mission and relevant goals for AI technology are understood and documented. MAP 1.4: The business value or context of business use has been clearly defined or – in the case of assessing existing AI systems – re-evaluated. MAP 1.5: Organizational risk tolerances are determined and documented.
```

**Câu trả lời của agent:** The MAP 1.2 team should reflect demographic diversity and broad domain and user experience expertise among its participants. Additionally, opportunities for interdisciplinary collaboration are prioritized [nist-ai-100-1-para-p031-c01].

**Citations:** ['nist-ai-100-1-para-p031-c01']

*Đoạn được trích `nist-ai-100-1-para-p031-c01` (trang 31):*
> MAP 1.2: Interdisciplinary AI actors, competencies, skills, and capacities for establishing context reflect demographic diversity and broad domain and user experience expertise, and their participation is documented. Opportunities for interdisciplinary collaboration are prioritized. MAP 1.3: The organization’s mission and relevant goals for AI technology are understood and documented. MAP 1.4: The business value or context of business use has been clearly defined or – in the case of assessing existing AI systems – re-evaluated. MAP 1.5: Organizational risk tolerances are determined and documented.

**Bạn chấm:**  Context = 2   Answer = 2   Citation support (từng citation: true/false) = true

**Lý do (tiếng Việt, lời của bạn):** Context có nguyên MAP 1.2 ở trang 31 (filter part2 đúng). Trả lời đúng và đủ, citation p031-c01 hỗ trợ trực tiếp cả ý phụ về hợp tác liên ngành.


## u-test-01 — câu thiếu evidence

**Câu hỏi:** How many hours of red-team testing does the framework require before an AI system is released?


### u-test-01 · BASELINE (BM25, không filter)

- Trạng thái: **abstain** · số lượt search: 2 · các query: ['red-team testing hours AI system release', 'red-team testing hours requirement AI system release']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(41, 'nist-ai-100-1-para-p041-c00'), (27, 'nist-ai-100-1-para-p027-c00'), (29, 'nist-ai-100-1-para-p029-c00')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p043-c03']

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p043-c03 | NIST.AI.100-1.pdf | page 43]
• Underdeveloped software testing standards and inability to document AI-based practices to the standard expected of traditionally engineered software for all but the simplest of cases. • Difficulty in performing regular AI-based software testing, or determining what to test, since AI systems are not subject to the same controls as traditional code development.
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Từ chối đúng và không bịa = ☒ có  ☐ không

**Lý do (tiếng Việt, lời của bạn):** Đã tìm PDF: red team, red-teaming, hours đều 0 lần; framework mang tính tự nguyện, không quy định số giờ. Agent từ chối, không thêm khẳng định nào. Baseline: context nhặt được chỉ là đoạn về kiểm thử phần mềm ở tr.43, không có số giờ.


### u-test-01 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **abstain** · số lượt search: 2 · các query: ['red-team testing hours AI system release', 'red-team testing hours requirement AI system release']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(41, 'nist-ai-100-1-para-p041-c00'), (27, 'nist-ai-100-1-para-p027-c00'), (29, 'nist-ai-100-1-para-p029-c00')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p043-c03']

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p043-c03 | NIST.AI.100-1.pdf | page 43]
• Underdeveloped software testing standards and inability to document AI-based practices to the standard expected of traditionally engineered software for all but the simplest of cases. • Difficulty in performing regular AI-based software testing, or determining what to test, since AI systems are not subject to the same controls as traditional code development.
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Từ chối đúng và không bịa = ☒ có  ☐ không

**Lý do (tiếng Việt, lời của bạn):** Đã tìm PDF: red team, red-teaming, hours đều 0 lần; framework mang tính tự nguyện, không quy định số giờ. Agent từ chối, không thêm khẳng định nào. Selected: cùng query và cùng context (tr.43) như baseline, vẫn từ chối đúng.


## u-test-02 — câu thiếu evidence

**Câu hỏi:** Which federated learning protocol does the AI RMF recommend?


### u-test-02 · BASELINE (BM25, không filter)

- Trạng thái: **abstain** · số lượt search: 2 · các query: ['federated learning protocol AI RMF recommendation', 'federated learning protocol recommendation']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(6, 'nist-ai-100-1-para-p006-c01'), (44, 'nist-ai-100-1-para-p044-c03'), (40, 'nist-ai-100-1-para-p040-c02')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p006-c01']

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p006-c01 | NIST.AI.100-1.pdf | page 6]
as an engineered or machine-based system that can, for a given set of objectives, generate outputs such as predictions, recommendations, or decisions influencing real or virtual environments. AI systems are designed to operate with varying levels of autonomy (Adapted from: OECD Recommendation on AI:2019; ISO /IEC 22989:2022).
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Từ chối đúng và không bịa = ☒ có  ☐ không

**Lý do (tiếng Việt, lời của bạn):** Đã tìm PDF: federated learning 0 lần (chỉ có 'Federal' trong tên cơ quan). Tài liệu không nêu giao thức nào. Agent từ chối, không bịa giao thức. Baseline: context là định nghĩa AI system ở tr.6, không liên quan giao thức.


### u-test-02 · SELECTED (BM25 + filter suy từ câu hỏi)

- Trạng thái: **abstain** · số lượt search: 2 · các query: ['federated learning protocol AI RMF recommendation', 'federated learning protocol recommendation']
- Bộ lọc đã áp dụng: None
- Top-3 tìm được: [(6, 'nist-ai-100-1-para-p006-c01'), (44, 'nist-ai-100-1-para-p044-c03'), (40, 'nist-ai-100-1-para-p040-c02')]
- Chunk thực sự nằm trong context: ['nist-ai-100-1-para-p006-c01']

**Context mà model đã nhìn thấy:**
```
[nist-ai-100-1-para-p006-c01 | NIST.AI.100-1.pdf | page 6]
as an engineered or machine-based system that can, for a given set of objectives, generate outputs such as predictions, recommendations, or decisions influencing real or virtual environments. AI systems are designed to operate with varying levels of autonomy (Adapted from: OECD Recommendation on AI:2019; ISO /IEC 22989:2022).
```

**Câu trả lời của agent:** Không đủ bằng chứng để trả lời.

**Đề xuất thô của model trước khi bị wrapper chuyển thành từ chối:** Không đủ bằng chứng để trả lời.  (citations: [])

**Citations:** []

**Bạn chấm:**  Từ chối đúng và không bịa = ☒ có  ☐ không

**Lý do (tiếng Việt, lời của bạn):** Đã tìm PDF: federated learning 0 lần (chỉ có 'Federal' trong tên cơ quan). Tài liệu không nêu giao thức nào. Agent từ chối, không bịa giao thức. Selected: không có filter nào được áp dụng, kết quả giống baseline và vẫn từ chối đúng.


---
# PHẦN D. Số liệu do chương trình đo (sự kiện, không phải đánh giá)

## D1. Agent trên dev, trước và sau khi sửa vòng lặp (22 câu: 20 có đáp án + 2 thiếu evidence)

| Lần chạy | Kết quả máy đo |
|---|---|
| Trước sửa, baseline (`dev_bm25_baseline_pre_fix.json`) | answered=10, abstain=11, error=1, số lượt search mỗi câu={0: 1, 1: 12, 3: 1, 4: 8}, chạm giới hạn search=8 |
| Trước sửa, selected (`dev_bm25_filter_selected_pre_fix.json`) | answered=8, abstain=14, error=0, số lượt search mỗi câu={1: 11, 4: 11}, chạm giới hạn search=11 |
| Sau sửa, baseline (`dev_bm25_baseline.json`) | answered=14, abstain=8, error=0, số lượt search mỗi câu={1: 16, 2: 6}, chạm giới hạn search=0 |
| Sau sửa, selected (`dev_bm25_dev_selected.json`) | answered=14, abstain=8, error=0, số lượt search mỗi câu={1: 16, 2: 6}, chạm giới hạn search=0 |

Ghi chú: bản trước sửa, baseline có 1 lần lỗi mạng (WinError 10054).

## D2. Những câu có đáp án bị từ chối trên dev (bản selected sau sửa) — dữ kiện từ trace

| Câu | Sự kiện cuối | Số lượt search | Chunk gốc trong top-3 | Chunk gốc trong context |
|---|---|---:|---|---|
| q01 | invalid_or_missing_citations | 2 | False | False |
| q03 | invalid_or_missing_citations | 2 | True | False |
| q04 | invalid_or_missing_citations | 2 | False | False |
| q06 | repeated_query_blocked | 1 | False | False |
| q07 | repeated_query_blocked | 1 | True | False |
| q19 | invalid_or_missing_citations | 1 | True | True |

Lưu ý khi đọc: với `invalid_or_missing_citations`, hãy mở `candidate_answer` trong trace để biết model tự từ chối hay trích sai; việc phân loại là của bạn.
