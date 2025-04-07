# 🧾 Legal Document Generator

This is a modular, Python-based boilerplate project for generating legal documents using **Jinja2** templates, **YAML**-based style sheets, and `python-docx`. It's designed to help law firms like yours create standardized, styled documents (like Letters of Representation) that integrate with Clio Manage merge fields.

---

## 📁 Project Structure



---

## 🚀 How It Works

1. **Templates**: Written in Jinja2, using Clio merge field syntax (`<<Matter.Client.Name>>`)
2. **Styles**: YAML files defining font, spacing, and alignment settings
3. **Context**: YAML test data files (mimic a Clio Matter)
4. **Script**: Renders Jinja2 + context, then applies styles to output `.docx`

---

## ✅ Usage (Windows)

1. Install Python 3.9+
2. From the project directory, run:

```bash
pip install -r requirements.txt
python generator.py

```
3. Check the output/ directory for the generated .docx file. 

## 🔄 Clio Merge Fields

Use Clio's merge field 
syntax: (`<<Matter.Client.Name>>`) (`<<Matter.Custom.DateOfLoss>>`)

You can test with content/example_context.yml, and later plug these templates directly into Clio Manage.

## 🔧 Dependancies

* ```python-docx``` - Word document creation
* ```jinja2``` - Template engine
* ```PyYAML``` - YAML parsing for context + style files

## 🧠 Tips

* Centralize style rules in styles/ to keep formatting consistent across docs
* Reuse utils/ for signature blocks, headers, tables, etc.
* Use the context files like test matters to preview formatting

## 📌 Status

🚧 In Progress
Actively developing new templates, formatting controls, and CLI support.


---

👤 Author 
Travis Crawford
IT Specialist | Legal Tech Developer
📧 solutionpartner@cfelab.com |
[linkedin](https://www.linkedin.com/in/crawford-t)
