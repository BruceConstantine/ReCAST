def back_previews_page_html_str():
    return '<html><head><script>history.go(-1)</script></head><body></body></html>'

def back_previews_page_html_str_with_alert(alert_str):
    return '<html><head><script>alert("'+alert_str+'");history.go(-1);</script></head><body></body></html>'
