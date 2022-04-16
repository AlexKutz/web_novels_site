document.addEventListener("DOMContentLoaded", () => main())

function main() {
    settingPanel()
    changeFontSize()
    changeTheme()
    arrowKeyPaging()
    changeLineHeight()
    resetBtn()
}

function settingPanel() {
    const panel = document.getElementById('settings')
    const toggleBtn = document.getElementById('settingsToggle')
    const svg = document.getElementById('settingsToggleSvg')
    panel.classList.add('disable-css-transitions')
    svg.classList.add('disable-css-transitions')
    if (window.localStorage.getItem('settingPanelClosed') == 'true') {
        panel.classList.add('settings_closed')
    }
    toggleBtn.onclick = () => {
        panel.classList.remove('disable-css-transitions')
        svg.classList.remove('disable-css-transitions')
        if (panel.classList.contains('settings_closed')) {
            panel.classList.remove('settings_closed')
            window.localStorage.setItem('settingPanelClosed', 'false')
        }
        else {
            panel.classList.add('settings_closed')
            window.localStorage.setItem('settingPanelClosed', 'true')
        }
    }
}

function arrowKeyPaging () {
    prev = document.getElementById('previousPage')
    next = document.getElementById('nextPage')
    document.addEventListener('keydown', (e) => {
        switch (e.keyCode) {
            case 37:
                prev.click()
                break;
            case 39:
                next.click()
                break;
        }
    })
}

function changeTheme() {
    const themesBox = document.getElementById('changeTheme')
    const bg = window.localStorage.getItem('readerColorSchemeBg')
    const color = window.localStorage.getItem('readerColorSchemeColor')

    if (bg && color) {
        document.body.style.backgroundColor = bg
        document.body.style.color = color
    }

    themesBox.onclick = e => {
        const theme = document.getElementById(e.target.id)
        if (theme) {
            const style = getComputedStyle(theme)
            document.body.style.backgroundColor = style.backgroundColor
            document.body.style.color = style.color
            window.localStorage.setItem('readerColorSchemeBg', style.backgroundColor)
            window.localStorage.setItem('readerColorSchemeColor', style.color)
        }
    }
}

function changeFontSize() {
    const changeBox = document.getElementById('changeFz')
    const readerFontSize = window.localStorage.getItem('readerFontSize')
    const text = document.getElementById('text')

    if (readerFontSize) {
        text.style.fontSize = readerFontSize
    }

    changeBox.onclick = e => {
        const fontSize = parseInt(getComputedStyle(text).fontSize.slice(0,2))
        if (e.target.dataset.action == 'increase' && fontSize < 40) {
            const newFontSize = `${fontSize + 1}px`
            text.style.fontSize = newFontSize
            window.localStorage.setItem('readerFontSize', newFontSize)
        } else if (e.target.dataset.action == 'decrease' && fontSize > 10) {
            const newFontSize = `${fontSize + -1}px`
            text.style.fontSize = newFontSize
            window.localStorage.setItem('readerFontSize', newFontSize)
        }
    }
}

function changeLineHeight() {
    const changeBox = document.getElementById('changeLineHeight')
    const readerLineHeight = window.localStorage.getItem('readerLineHeight')
    const text = document.getElementById('text')

    if (readerLineHeight) {
        text.style.lineHeight = readerLineHeight
    }

    changeBox.onclick = e => {
        const lineHeight = parseInt(getComputedStyle(text).lineHeight.slice(0,2))
        if (e.target.dataset.action == 'increase' && lineHeight < 40) {
            const newLineHeight = `${lineHeight+1}px`
            text.style.lineHeight = newLineHeight
            window.localStorage.setItem('readerLineHeight', newLineHeight)
        } else if (e.target.dataset.action == 'decrease' && lineHeight > 11) {
            const newLineHeight = `${lineHeight-1}px`
            text.style.lineHeight = newLineHeight
            window.localStorage.setItem('readerLineHeight', newLineHeight)
        }
    }
}

function resetBtn() {
    const button = document.getElementById('reset')
    button.onclick = () => {
        localStorage.removeItem('readerLineHeight')
        localStorage.removeItem('readerFontSize')
        localStorage.removeItem('readerColorSchemeBg')
        localStorage.removeItem('readerColorSchemeColor')
        location.reload();
    }
}