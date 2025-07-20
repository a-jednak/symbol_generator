# Lock screen symbol generator
### 🎉 Deployed using streamlit you can try it [here](https://lockscreensymbolgenerator.streamlit.app) 🎉
---
Inspired by that one time I forgot the symbol for my phone and was trying to access it for multiple hours - I have made this simple web app.

## 💡 Features

- 3x3 dot grid (0 to 8)
- Auto-inserts "middle dots" (like 0 to 8 auto-inserting 4)
- Customizable:
  - Start sequence
  - End sequence
  - Symbol length (4–9 dots)
- Random pattern generation if no inputs are given
- Visual rendering of the pattern using `matplotlib`
- Web interface via Streamlit


## 📦 Requirements
If you'd like to deploy it locally install dependecies with:
```bash
pip install -r requirements.txt
```
and run in your terminal with:
```bash
streamlit run symbol_generator.py
```





