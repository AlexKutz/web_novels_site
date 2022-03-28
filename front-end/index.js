document.addEventListener("DOMContentLoaded", () => main())

function main() {
    const backToTop = new BackToTop("backToTop", "backToTop_hide")
    const DarkModeBtn = new DarkMode("changeColorScheme__sun", "changeColorScheme__moon", "changeColorScheme__sun_hide", "changeColorScheme__moon_hide")
    if (document.getElementById('search-form') != null) {
        const search = new Search('search-form', 'section')
    }
    Catalog()
    authenticationMenu()
    const tagSortForm = document.getElementById('tagSort')
    if (tagSortForm != null) {
        tagPageSorting(tagSortForm)
    }
    const container = document.getElementById('profileEmail')
    if (container != null) {
        setAccountEmail(container)
    }
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
}

function setAccountEmail(block, btn) {
    //Change link to input field on click. Send request to set email on server.
    const container = block
    const buttonChange = document.getElementById('setEmailBtn')
    const buttonConfirm = document.getElementById('emailConfirmBtn')
    const containerText = container.innerText.split('\n')[0]
    const inputField =
        `
        <input type='text' class='profile-email__input' autofocus> 
        `
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    buttonChange.onclick = () => {
        container.innerHTML = inputField
        const input = container.children[0]
        input.focus()
        input.addEventListener('input', () => {
            if (validateEmail(input.value)) {
                input.classList.remove('profile-email__input_invalid')
                input.classList.add('profile-email__input_valid')
            } else {
                input.classList.remove('profile-email__input_valid')
                input.classList.add('profile-email__input_invalid')
            }
        })
        input.addEventListener('focusout', () => {
            if (input.value.trim() == '') {
                container.innerHTML = containerText
                container.appendChild(buttonChange)
                container.appendChild(buttonConfirm)
            } else {
                if (!validateEmail(input.value)) {
                    return ''
                }
                container.innerHTML = '<div class="dot-pulse"></div>'
                fetch('/accounts/email_change', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    mode: 'same-origin',
                    body: JSON.stringify({'new_email': input.value})
                })
                    .then((response) => {
                        if (!response.ok) {
                            throw response
                        }
                        return response.json()
                    })
                    .then(resp => {
                        container.innerHTML = resp.new_email
                        container.appendChild(buttonChange)
                        container.appendChild(buttonConfirm)

                    })
                    .catch(err => {
                        err.json().then(response => {
                            container.innerHTML = ''
                            container.appendChild(input)
                            const message = document.createElement('div')
                            message.innerHTML = response.message.new_email
                            message.style.marginTop = '10px'
                            container.appendChild(message)
                        })
                    })

            }
        })
    }
}

function tagPageSorting(form) {
    `Sort bookCards on tag page using fetch ajax`
    const bookCards = document.getElementById('tagCards')
    const loading = document.getElementById('loading')
    const radio = form.sort
    form.onclick = (e) => {
        if (e.target.dataset.input == 'true') {
            bookCards.innerHTML = ''
            loading.style.display = 'block'
            let params = {
                'sort_by': e.target.value
            }
            getFilteredBooksFromServer(params)
                .then((books) => {
                    console.log(params)
                    console.log(books)
                    renderPage(books, bookCards)
                    loading.style.display = 'none'
                })
                .catch((e) => {
                    console.warn(e)
                    loading.style.display = 'none'
                })
        }

    }
}

function getFilteredBooksFromServer(params) {
    return fetch('/get_filtered_books_JSON/', {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify(params)
    })
        .then((response) => {
            return response
        }).then((res) => res.json())

}

function renderPage(json, whereToRender) {
    `Get list of dictionaries with book data and render it on page`
    let html = ''
    for (let book of json) {
        html += createBookCard(book)
    }
    whereToRender.innerHTML = html
}


function createBookCard(novelData) {
    let tags = ''
    for (let tag of novelData.tags) {
        tags += `<a href="#" class="meta__tag bookCard__tag">${tag.name}</a>`
    }
    return `
        <div class="bookCard">
        <div class="bookCard__container">
          <div class="bookCard__column-1">
            <a href="/books/${novelData.id}" class="bookCard__image noselect">
              <img src="${novelData.book_image}" alt="Cover of the book">
            </a>
            <div class="bookCard__buttons noselect">
              <a href="/books/${novelData.id}" class="btn bookCard__btn btn-border-anim">Читать</a>
            </div>
          </div>
          <div class="bookCard__column-2">
            <a href="/books/${novelData.id}" class="bookCard__title">${novelData.title}</a>
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
        <div class="bookCard__uploadTime">${novelData.timesince}</div>
      </div>`
}

function authenticationMenu() {
    const toggleIcon = document.getElementById('accountIco')
    const dropdown = document.querySelector('.dropdown')
    document.body.onclick = (e) => {
        // if (dropdown.classList.contains('dropdown_active')) {
        //     dropdown.classList.remove('dropdown_active')
        // }
        // if (e.target.dataset)
        if (e.target.dataset.menu != 'true') {
            dropdown.classList.remove('dropdown_active')
        }
    }
    toggleIcon.onclick = () => {
        dropdown.classList.toggle('dropdown_active')
    }

}


import SlimSelect from 'slim-select'

function Catalog() {
    const bookCards = document.querySelector('.catalog-books')
    const loading = document.getElementById('loading')
    if (bookCards) {
        const includeTags = new SlimSelect({
            select: '.include-tags', searchPlaceholder: 'Поиск',
        })
        const excludeTags = new SlimSelect({
            select: '.exclude-tags', searchPlaceholder: 'Поиск',
        })
        const sortBy = new SlimSelect({
            select: '.catalog-sortby', showSearch: false
        })
        const chaptersSelect = new SlimSelect({
            select: '.catalog-chapter', showSearch: false
        })
        const chaptersInput = document.getElementById('chaptersInput')
        const form = document.getElementById('filters-form')
        form.onsubmit = (e) => {
            e.preventDefault()
            loading.style.display = 'block'
            let params = {
                'include_tags': includeTags.selected(),
                'exclude_tags': excludeTags.selected(),
                'sort_by': sortBy.selected(),
                'chapters_more_less_select': chaptersSelect.selected(),
                'chaptersNumber': chaptersInput.value,
            }
            getFilteredBooksFromServer(params)
                .then((books) => {
                    renderPage(books, bookCards)
                    loading.style.display = 'none'
                })
                .catch((e) => {
                    console.warn(e)
                    loading.style.display = 'none'
                })
        }
    }

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


    createUrl(data) {
        // Return url with parameters for request
        let url = new URL("search/", location.protocol.concat("//").concat(window.location.host))
        for (let [key, value] of Object.entries(data)) {
            url.searchParams.append(key, value)
        }
        return url
    }


    addEventListeners() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault()
            const inputValue = this.form.childNodes[1].value
            this.sendRequest(this.createUrl({'q': inputValue}))
                .then(data => {
                    renderPage(data, this.placeOnPage)
                })
                .catch(error => console.log(error))
        })
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
