
// Just delay a little bit
export const delay = (timeout, callback) => new Promise(resolve => setTimeout(resolve, timeout, callback))

// Scroll the window automatically to an already-rendered element on the page
export const scrollTo = (elementId) => document.getElementById(elementId).scrollIntoView()
