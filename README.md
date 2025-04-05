# 🧾 Legal Document Generator

This is a modular, Python-based boilerplate project for generating legal documents using **Jinja2** templates, **YAML**-based style sheets, and `python-docx`. It's designed to help law firms like yours create standardized, styled documents (like Letters of Representation) that integrate with Clio Manage merge fields.

---

## 📁 Project Structure


---

## 🚀 How It Works

1. **Templates**: Written in Jinja2, they contain Clio merge field placeholders (e.g., `<<Matter.Client.Name>>`).
2. **Styles**: YAML files define paragraph, font, and margin settings.
3. **Context**: YAML file that temporarily fills in merge values for previewing/testing.
4. **Document Rendering**:
   - The script renders the Jinja2 template with values from `content/`.
   - Then it applies formatting using the corresponding style profile.
   - Output is saved to the `output/` folder.

---

## ✅ Usage (Windows)

1. Install Python (3.9+ recommended)
2. Run the following from the project directory:

```bash
pip install -r requirements.txt
python generator.py
```
3. Check the output/ directory for the generated .docx file. 

## 🔄 Clio Merge Fields

To prepare your templates for use within Clio Manage, use Clio's merge field syntax: 

Example:

```
<<Matter.Client.Name>>
<<Matter.Custom.DateOfLoss>>
```

These will be dynamically filled by Clio when the document is generated inside a client matter.

## 🔧 Dependancies

* ```python-docx``` - DOCX creation and styling
* ```jinja2``` - Content Templating
```PyYAML``` - Style and context configuration

## 🧠 Tips

* Keep styles centralized so multiple templates can share formatting rules
* Use placeholder-friendly text in content files for testing
* Expand ```utils/style_applier.py``` to support more advanced styling like tables and headers.

## 📌 Status

In progress - new templates, advanced formatting options, and CLI enhancements are being added weekly. 


---

## 👤 Author

**Travis Crawford**  
IT Specialist | Legal Tech Developer  
[my email](solutionpartner@cfelab.com)
[linkedin](https://www.linkedin.com/in/t-crawford29)
