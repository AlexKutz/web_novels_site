document.addEventListener("DOMContentLoaded", () => main())

function main() {
    backToTop = new BackToTop("backToTop", "backToTop_hide")
    DarkModeBtn = new DarkMode("changeColorScheme__sun", "changeColorScheme__moon", "changeColorScheme__sun_hide", "changeColorScheme__moon_hide")
    search = new Search('search-form', 'section')
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
            } else {
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
        } else {
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

    addEventListeners() {
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

class Search {
    constructor(formId, placeOnPageId) {
        this.form = document.getElementById(formId)
        this.placeOnPage = document.getElementById(placeOnPageId)
        this.addEventListeners()
    }

    addEventListeners() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault()
            this.sendRequest(this.createUrl())
                .then(data => {
                    this.renderPage(data)
                })
                .catch(error => console.log(error))
        })
    }


    createUrl() {
        // Return url with parameters for request
        const inputValue = this.form.childNodes[1].value
        let url = new URL("search/", location.protocol.concat("//").concat(window.location.host))
        url.searchParams.append('q', inputValue)
        return url
    }

    createBookCard(novelData) {
        let tags = ''
        for (let tag of novelData.tags) {
            tags += `<a href="#" class="meta__tag bookCard__tag">${tag.name}</a>`
        }
        return `
        <div class="bookCard">
        <div class="bookCard__container">
          <div class="bookCard__column-1">
            <a href="{% url 'novels' novel.id %}" class="bookCard__image noselect">
              <img src="${novelData.book_image}" alt="Cover of the book">
            </a>
            <div class="bookCard__buttons noselect">
              <a href="{% url 'novels' novel.id %}" class="btn bookCard__btn btn-border-anim">Читать</a>
            </div>
          </div>
          <div class="bookCard__column-2">
            <a href="{% url 'novels' novel.id %}" class="bookCard__title">${novelData.title}</a>
            ${novelData.adult_only ? '<span className="bookCard__adultOnly"> [R18+]</span>' : ''}
            <div class="bookCard__metaData">
              <a href="#" class="bookCard__author">${novelData.author.name}</a>
              <span class="bookCard__numWords">
              ${novelData.words}
              </span>
              <span class="bookCard__status">${novelData.status.name.charAt(0).toUpperCase() + novelData.status.name.slice(1)}</span>
            </div>
            <div class="bookCard__tags">` + tags + `</div>
            <div class="bookCard__description">
              ${novelData.description}
            </div>
          </div>
        </div>
        <div class="bookCard__uploadTime">${novelData.timesince} назад</div>
      </div>`
    }

    renderPage(data) {
        let bookCards = '<h2 class="sectionTitle">Результаты поиска</h2>'
        console.log(data)
        for (let novel of data) {
            bookCards += this.createBookCard(novel)
        }
        this.placeOnPage.innerHTML = bookCards
    }

    sendRequest(url) {
        // Function which send GET request with search query on server and return Parsed JSON

        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest()

            xhr.open('GET', url)

            xhr.responseType = 'json'

            xhr.onload = () => {
                if (xhr.status >= 400) {
                    reject(xhr.response)
                } else {
                    resolve(xhr.response)
                }
            }

            xhr.onerror = (e) => {
                reject(xhr.response)
            }

            xhr.send()
        })

    }
}