# 🧾 Document Table Terminology Cheat Sheet  
*Understand the difference between technical structure and semantic meaning in legal document tables.*

---

## 📐 Technical Terms (Used in Code / python-docx)

| Term       | Meaning                                                             | Example                                     |
|------------|---------------------------------------------------------------------|---------------------------------------------|
| **Table**    | The overall grid structure                                         | `table = doc.add_table()`                   |
| **Row**      | A horizontal group of cells                                        | `table.rows[0]` = first row                 |
| **Column**   | A vertical slice of the table                                      | 1st column contains all labels              |
| **Cell**     | A single box where data goes (row x column intersection)          | `table.cell(0, 1)` = first row, second column |

---

## 🏷️ Semantic Terms (Used in Legal Documents & UX)

| Term       | Meaning                                                             | Example                                     |
|------------|---------------------------------------------------------------------|---------------------------------------------|
| **Field**     | A logical data element or category                                 | “Claim Number” is a field                   |
| **Label**     | The visible title or name of a field                              | Label: “Claim No:”                          |
| **Value**     | The content assigned to a label                                   | Value: `A123456789`                         |
| **Grid**      | A visual representation of data in table layout (used interchangeably) | “RE info grid” = Claim info table       |

---

## 🔄 Mapping Between Technical and Semantic

| Code Term (python-docx) | Semantic Concept |
|--------------------------|------------------|
| `table.cell(0, 0)`       | Label: “Claimant” |
| `table.cell(0, 1)`       | Value: “Jane Doe” |

---

## 🧠 Why It Matters

- Developers use **rows/cells** to position content
- Legal/operations teams use **fields/labels/values** to describe content
- Document engineers (like you!) bridge that gap to create scalable, clean systems

