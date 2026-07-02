with open('app.py', 'r') as f:
    content = f.read()

# Find the escapeHtml function and fix it
old = """function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&', '<': '<', '>': '>', '"': '"', "'": ''' }[ch]));
    }"""

new = """function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, ch => ({ '&': '&', '<': '<', '>': '>', '"': '"', "'": ''' }[ch]));
    }"""

if old in content:
    content = content.replace(old, new)
    with open('app.py', 'w') as f:
        f.write(content)
    print('Fixed escapeHtml!')
else:
    print('Pattern not found')
    idx = content.find('function escapeHtml')
    if idx >= 0:
        print(repr(content[idx:idx+200]))