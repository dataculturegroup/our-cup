
export const delay = (t, v) => new Promise(resolve => setTimeout(resolve, t, v))

export const scrollTo = (elementId) => document.getElementById(elementId).scrollIntoView()
