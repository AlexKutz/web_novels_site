document.addEventListener("DOMContentLoaded", () => main())

function main() {
    backToTop = new BackToTop("backToTop", "backToTop_hide")
    DarkModeBtn = new DarkMode("changeColorScheme__sun", "changeColorScheme__moon", "changeColorScheme__sun_hide", "changeColorScheme__moon_hide")
}

class BackToTop {
    constructor(btnClass, hideClass) {
        this.btn = document.querySelector("." + btnClass)
        if (!this.btn) {
            throw `Button (${btnClass}) not found`
        } else {
            this.hideClass = hideClass
            this.addEventListeners()
            this.hideBtn(this.btn, this.hideClass)
        }
    }
    addEventListeners() {
        document.addEventListener('scroll', () => {
            if (window.scrollY > outerHeight + outerHeight / 3) {
                this.showBtn(this.btn, this.hideClass)
            }
            else {
                this.hideBtn(this.btn, this.hideClass)
            }
        })
        this.btn.addEventListener('click', () => {
            this.scrollToTop()
        })
    }
    showBtn(button, hideClass) {
        button.classList.remove(hideClass)
    }
    hideBtn(button, hideClass) {
        button.classList.add(hideClass)
    }
    scrollToTop = () => {
        const c = document.documentElement.scrollTop || document.body.scrollTop;
        if (c > 0) {
            window.requestAnimationFrame(this.scrollToTop);
            window.scrollTo(0, c - c / 8);
        }
    }

}

class DarkMode {
    constructor(lightBtnClass, darkBtnClass, lightHideClass, darkHideClass) {
        this.lightBtn = document.querySelector("." + lightBtnClass)
        this.darkBtn = document.querySelector("." + darkBtnClass)
        this.lightHideClass = lightHideClass
        this.darkHideClass = darkHideClass
        this.lightMode = window.localStorage.getItem('lightMode')
        if (this.lightMode == 'light') {
            document.documentElement.dataset.colorscheme = 'light'
        } else if (this.lightMode == 'dark') {
            document.documentElement.dataset.colorscheme = 'dark'
        } else {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                window.localStorage.setItem('lightMode', 'dark')
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                window.localStorage.setItem('lightMode', 'light')
            }
        }
        if (!this.lightBtn || !this.darkBtn) {
            throw `Can't find button (${lightBtnClass}, ${darkBtnClass})`
        }
        else {
            if (document.documentElement.dataset.colorscheme == "light") {
                this.show(this.darkBtn, this.darkHideClass)
            } else {
                this.show(this.lightBtn, this.lightHideClass)
            }
        }
        this.addEventListeners()
    }
    show(btn, hideClass) {
        btn.classList.remove(hideClass)
    }
    hide(btn, hideClass) {
        btn.classList.add(hideClass)
    }
    addEventListeners () {
        this.darkBtn.onclick = () => {
            this.hide(this.darkBtn, this.darkHideClass)
            this.show(this.lightBtn, this.lightHideClass)
            document.documentElement.dataset.colorscheme = "dark"
            window.localStorage.setItem('lightMode', 'dark')
        }
        this.lightBtn.onclick = () => {
            this.hide(this.lightBtn, this.lightHideClass)
            this.show(this.darkBtn, this.darkHideClass)
            document.documentElement.dataset.colorscheme = "light"
            window.localStorage.setItem('lightMode', 'light')
        }
    }
}