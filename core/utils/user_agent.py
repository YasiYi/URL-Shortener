def detect_device_type(user_agent: str) -> str:
    return "Mobile" if "Mobile" in user_agent else "Desktop"

def detect_browser(user_agent: str) -> str:
    ua = user_agent.lower()
    if "chrome" in ua and "edg" not in ua:
        return "Chrome"
    if "firefox" in ua:
        return "Firefox"
    if "safari" in ua and "chrome" not in ua:
        return "Safari"
    if "edg" in ua:
        return "Other"
