import SlimSelect from 'slim-select'
import Croppie from './plugins/croppie'
import tingle from './plugins/tingle'
import FastAverageColor from 'fast-average-color'

document.addEventListener('DOMContentLoaded', () => main())

function main () {
  BackToTop('backToTop', 'backToTop_hide')
  DarkMode('changeColorScheme__sun', 'changeColorScheme__moon', 'changeColorScheme__sun_hide', 'changeColorScheme__moon_hide')
  if (document.querySelector('.catalog-books')) {
    catalog()
    renderPage({
      sort_by: '-created_at',
      pagination_options: {
        page: 1,
        books_per_page: 16
      }
    })
  }
  if (document.querySelector('.last-books')) {
    index()
  }

  if (document.querySelector('.author-books')) {
    authorBooksPage()
  }

  if (document.getElementById('accountIco')) {
    authenticationMenu()
  }
  if (document.getElementById('tagSort')) {
    tagPageSorting()
  }
  const container = document.getElementById('profileEmail')
  if (container != null) {
    setAccountEmail(container)
  }
  if (document.getElementById('imageInput') != null) {
    changeProfileImage()
  }
  const emailConfirmBtn = document.getElementById('emailConfirmBtn')
  if (emailConfirmBtn) {
    emailConfirmBtn.onclick = () => {
      sendActivationRequest()
    }
  }
  if (document.querySelector('.info-bg')) {
    changeBackgroundOnNovePage()
  }

  if (document.getElementById('changeTabsForm')) {
    changeTab()
  }

  if (document.getElementById('bookShelfAdd') || document.getElementById('bookShelfRemove')) {
    toggleBookshelf()
  }

  const commentForm = document.getElementById('commentForm')
  if (document.getElementById('comments')) {
    const comments = new Comments()
    comments.update()
    if (commentForm) {
      commentForm.onsubmit = (e) => {
        e.preventDefault()
        comments.postComment(commentForm)
      }
    }
  }
}

function index () {
  const renderOptions = {
    sort_by: '-created_at',
    pagination_options: {
      page: 1,
      books_per_page: 16
    }
  }
  renderPage(renderOptions)
  search('search-form')
}

function search (formId) {
  const form = document.getElementById(formId)
  addEventListeners()

  function addEventListeners () {
    form.addEventListener('submit', (e) => {
      e.preventDefault()
      const renderOptions = {
        sort_by: '-created_at',
        pagination_options: {
          page: 1,
          books_per_page: 16
        },
        filters: {
        }
      }
      const inputValue = form.childNodes[1].value
      const title = inputValue.match(/"(.*?)"/)
      const author = inputValue.match(/\((.*?)\)/)
      if (title) {
        renderOptions.filters.title = title[1].trim()
      }
      if (author) {
        renderOptions.filters.author = author[1].trim()
      }

      const re = /\[(.*?)\]/g
      const result = []
      let current
      // eslint-disable-next-line no-cond-assign
      while (current = re.exec(inputValue)) {
        result.push(current.pop())
      }
      if (result) {
        renderOptions.filters.include_tags = result
      }
      if (result.length === 0 && !title && !author) {
        return
      }
      renderPage(renderOptions)
    })
  }
}

function authorBooksPage () {
  const author = document.getElementById('author').innerText
  const renderOptions = {
    sort_by: '-created_at',
    pagination_options: {
      page: 1,
      books_per_page: 16
    },
    filters: {
      author
    }
  }
  renderPage(renderOptions)
}

function renderPaginator (pageData, options) {
  const paginator = document.getElementById('pagination')
  paginator.innerHTML = ''
  const linksContainer = document.createElement('div')
  linksContainer.classList.add('step-links')
  linksContainer.classList.add('noselect')
  const paginatorConstruction = pageData.elided_page_range
  const lastPageNumber = paginatorConstruction[paginatorConstruction.length - 1]
  const pageNumber = pageData.number
  if (pageData.has_previous) {
    const prevBtn = document.createElement('span')
    prevBtn.innerText = '<'
    prevBtn.onclick = () => {
      options.pagination_options.page = pageNumber - 1
      renderPage(options)
    }
    linksContainer.append(prevBtn)
  }
  for (const button of paginatorConstruction) {
    const doc = document.createElement('span')
    if (button === pageNumber) {
      doc.classList.add('pagination__current-page')
      doc.innerText = button
      linksContainer.append(doc)
      continue
    }
    if (button === '…') {
      if (pageNumber < lastPageNumber - 3 && linksContainer.querySelector('.pagination__current-page') != null) {
        doc.classList.add('pagination__rewind_forward')
        doc.onclick = () => {
          options.pagination_options.page = pageNumber + 4
          renderPage(options)
        }
      }
      if (pageNumber > 4 && linksContainer.querySelector('.pagination__current-page') == null) {
        doc.classList.add('pagination__rewind_back')
        doc.onclick = () => {
          options.pagination_options.page = pageNumber - 4
          renderPage(options)
        }
      }
    } else {
      doc.innerText = button
      doc.onclick = (e) => {
        options.pagination_options.page = button
        renderPage(options)
      }
    }
    linksContainer.append(doc)
  }
  if (pageData.has_next) {
    const nextBtn = document.createElement('span')
    nextBtn.innerText = '>'
    nextBtn.onclick = () => {
      options.pagination_options.page = pageNumber + 1
      renderPage(options)
    }
    linksContainer.append(nextBtn)
  }

  paginator.appendChild(linksContainer)
}

class Comments {
  constructor () {
    this.commentsBox = document.getElementById('comments')
    this.csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    this.novelId = document.getElementById('novelId').innerText
  }

  update () {
    fetch('/get_comments_json/', {
      method: 'POST',
      headers: {
        Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': this.csrftoken
      },
      mode: 'same-origin',
      body: JSON.stringify({ novelId: this.novelId })
    })
      .then(response => {
        if (response.ok) {
          return response.json()
        } else {
          throw new Error('Server response not OK')
        }
      })
      .then(json => {
        const isAuth = document.getElementById('auth') != null
        this.commentsBox.innerHTML = this.renderComments(json, '', 0, isAuth)
        const comments = this.commentsBox.querySelectorAll('.comment')
        if (isAuth) {
          comments.forEach(comment => {
            this.addEventListener(comment)
          })
        }
      })
      .catch(err => {
        console.error(err)
      })
  }

  /**
   * Sets an event listener on like and response buttons to specified comment
   * @param comment
   */
  addEventListener (comment) {
    comment.addEventListener('click', (e) => {
      e.stopPropagation()
      const id = comment.querySelector('.comment__id').innerText
      if (e.target.dataset.type === 'like') {
        this.sendLikeRequest(id)
      }
      if (e.target.dataset.type === 'response') {
        this.addCommentParentToForm(id, comment)
      }
    })
  }

  addCommentParentToForm (id, comment) {
    let parentBlock = document.getElementById('rateTextareaParentBlock')
    const textarea = document.getElementById('rateTextarea')
    const formInputParent = document.getElementById('commentParent')
    const container = document.getElementById('commentTextAreaContainer')
    const placeholder = textarea.placeholder
    if (parentBlock) {
      parentBlock.innerHTML = ''
    } else {
      parentBlock = document.createElement('span')
    }
    formInputParent.value = id
    textarea.placeholder = ''
    parentBlock.id = 'rateTextareaParentBlock'
    parentBlock.innerHTML = `Ответить пользователю ${comment.querySelector('.comment__name').innerText} <svg fill="#000000" viewBox="0 0 24 24" width="16px" height="16px"><path d="M 4.7070312 3.2929688 L 3.2929688 4.7070312 L 10.585938 12 L 3.2929688 19.292969 L 4.7070312 20.707031 L 12 13.414062 L 19.292969 20.707031 L 20.707031 19.292969 L 13.414062 12 L 20.707031 4.7070312 L 19.292969 3.2929688 L 12 10.585938 L 4.7070312 3.2929688 z"/></svg>`
    container.insertAdjacentElement('afterbegin', parentBlock)
    window.scrollTo(0, textarea.offsetTop - textarea.offsetHeight)
    textarea.focus()

    parentBlock.onclick = () => {
      formInputParent.value = ''
      textarea.placeholder = placeholder
      parentBlock.remove()
    }
  }

  sendLikeRequest (id) {
    // Sends a request to the server to change like state for the current user
    fetch('/toggle_comment_like/', {
      method: 'POST',
      headers: {
        Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': this.csrftoken
      },
      mode: 'same-origin',
      body: JSON.stringify({ commentId: id })
    })
      .then(response => {
        if (response.ok) {
          return response.json()
        } else {
          throw new Error('Server response not OK')
        }
      })
      .then(json => {
        const heartBtn = document.getElementById(`heart${id}`)
        const totalLikes = document.getElementById(`likeTotal${id}`)
        if (json.is_liked === true) {
          heartBtn.classList.add('heart_pressed')
        } else if (json.is_liked === false) {
          heartBtn.classList.remove('heart_pressed')
        }
        if (json.totalLikes > 0) {
          totalLikes.innerText = json.totalLikes
        } else {
          totalLikes.innerText = ''
        }
      })
      .catch(err => {
        console.error(err)
      })
  }

  makeHeart (likeState, id) {
    return `<svg id="heart${id}" data-type="like" style="max-width:20px; max-height:23px; width:100%; height:100%;" class='heart ${likeState ? 'heart_pressed' : ''}' viewBox="0 0 34 29.7"><path data-type="like" d="M17,28.4C4.41,18.15,1,14.58,1,9A8,8,0,0,1,9,1c3.6,0,5.63,1.94,7.25,3.76l.75.85.75-.85C19.37,2.94,21.39,1,25,1a8,8,0,0,1,8,8C33,14.58,29.59,18.15,17,28.4Z"/><path data-type="like" d="M9,2A7,7,0,0,0,2,9c0,5.1,3.2,8.5,15,18.1C28.8,17.5,32,14.1,32,9a7,7,0,0,0-7-7c-3.5,0-5.4,2.1-6.9,3.8L17,7.1,15.9,5.8C14.4,4.1,12.5,2,9,2Z" style="fill:none"/></svg>`
  }

  renderComments (comments, lstComment = '', inh, isAuth) {
    let html = ''
    inh += 1
    for (const comment of comments) {
      html += `
                      <div class="comment" id="comment${comment.id}">
                        <div class="comment__id hidden" style="display:none;">${comment.id}</div>
                        <div class="flex-container">
                            <div class="comment__avatar">
                                <img src="${comment.user.image}" class="authenticated__account-image"
                                     id="headerAccImage">
                            </div>
                            <div class="comment__data">
                                <span class="comment__name">${comment.user.username}</span>
                                <span class="comment__created noselect">${comment.created_on}</span>
                                ${lstComment.parent
        ? `
                                    <div class="comment__reply-msg ${inh > 1 ? 'mobile-display-on' : ''} ${inh > 4 ? 'display-on' : ''}">
                                        <svg id="Layer_1" style="max-width: 15px; max-height: 15px; display: inline-block" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 879.19 860.19"><path d="M863.49,979.67s15.6,4.1,15.7-19.6c-.1-23.8-.1-135.5-.1-152.5.1-16.8-13-16.5-13-16.5H305.59c0-191.2,0-318.05-.1-369.25.1-24.4,0-40.2,0-40.2h95.1c36.7,0,9-27.6,9-27.6s-159.1-206-180.8-227.8c-15.8-15.6-30.6,1.9-30.6,1.9L11.59,348.92S-16,375.12,14,375h102.9s0,17.8.1,44.9c-.1,53.2-.1,180.75,0,371.15h-.2v176.8c.3,4.3,3.3,11,16.9,11.8h729.8Z" transform="translate(0 -119.75)"/></svg>
                                        <span>Ответ на коментарий [${lstComment.user.username}]</span>
                                    </div>`
        : ''}
                                <span class="comment__text">${comment.text}</span>
                            </div>
                        </div>
                        <span class='comment__buttons noselect'>
                            ${comment.is_liked ? this.makeHeart(true, comment.id) : this.makeHeart(false, comment.id)}
                            <span id="likeTotal${comment.id}"> ${comment.totalLikes ? comment.totalLikes : ''}</span>
                            ${isAuth ? '<span class="comment__buttons-response" data-type="response">Ответить</span>' : ''}
                        </span>
                        
                        ${// eslint-disable-next-line eqeqeq
        comment.replies != false
          ? `<button class="toggle-reply-btn noselect" 
                        onclick="toggleRepliesHidden(rep${comment.id})"><svg id="Layer_1" style='max-width:15px;' data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 448"><path d="M503.69,322.16l-176,152C312.28,487.45,288,476.65,288,456V375.93C127.37,374.09,0,341.9,0,189.67,0,128.23,39.58,67.37,83.33,35.54c13.66-9.93,33.11,2.54,28.08,18.63C66.07,199.19,132.92,237.68,288,239.92V152c0-20.7,24.3-31.45,39.69-18.16l176,152A24,24,0,0,1,503.69,322.16Z" transform="translate(0 -32)"/></svg>Посмотреть ответы</button>
                        <div class="replies hidden ${inh > 1 ? 'mobile-margin-off' : ''} ${inh > 4 ? 'margin-off' : ''}" id=rep${comment.id}>
                            ${this.renderComments(comment.replies, comment, inh, isAuth)}
                        </div>
                        `
          : ''}
                    </div>
                `
    }
    return html
  }

  postComment (form) {
    const data = this.getDataFromForm(form)
    const novelId = document.getElementById('novelId').innerText
    data.novel_id = novelId
    fetch('/post_comment/', {
      method: 'POST',
      headers: {
        Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': this.csrftoken
      },
      mode: 'same-origin',
      body: JSON.stringify(data)
    })
      .then(response => {
        if (response.ok) {
          return response.json()
        } else {
          throw new Error('Server response not OK')
        }
      })
      .then(json => {
        const comments = new Array(json)
        const isAuth = true
        const html = this.renderComments(comments, '', 0, isAuth)
        if (json.parent) {
          this.update()
        } else {
          document.getElementById('comments').insertAdjacentHTML('afterbegin', html)
          this.addEventListener(document.getElementById(`comment${json.id}`))
        }
      })
      .catch(err => {
        console.error(err)
      })
  }

  getDataFromForm (form) {
    const data = {}
    form.querySelectorAll('input').forEach(input => {
      if (input.value) {
        data[input.name] = input.value
      }
    })
    form.querySelectorAll('textarea').forEach(textarea => {
      if (textarea.value) {
        data[textarea.name] = textarea.value
      }
    })
    return data
  }
}

function toggleRepliesHidden (elem) {
  if (Object.getPrototypeOf(elem) === HTMLCollection.prototype) {
    Array.from(elem).forEach(item => item.classList.toggle('hidden'))
  } else {
    elem.classList.toggle('hidden')
  }
}

window.toggleRepliesHidden = toggleRepliesHidden

function toggleBookshelf () {
  const bookshelfAdd = document.getElementById('bookShelfAdd')
  const bookshelfRemove = document.getElementById('bookShelfRemove')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  const novelId = document.getElementById('novelId').innerText
  bookshelfAdd.onclick = () => {
    fetch('/add_to_bookshelf/', {
      method: 'POST',
      headers: {
        Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
      },
      mode: 'same-origin',
      body: JSON.stringify({ novelId })
    })
      .then(response => {
        if (!response.ok) {
          throw response
        }
        bookshelfAdd.style.display = 'none'
        bookshelfRemove.style.display = 'flex'
      })
      .catch(error => {
        throw new Error(error)
      })
  }
  bookshelfRemove.onclick = () => {
    fetch('/remove_from_bookshelf/', {
      method: 'POST',
      headers: {
        Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
      },
      mode: 'same-origin',
      body: JSON.stringify({ novelId })
    })
      .then(response => {
        if (!response.ok) {
          throw response
        }
        bookshelfRemove.style.display = 'none'
        bookshelfAdd.style.display = 'flex'
      })
      .catch(error => {
        throw new Error(error)
      })
  }
}

function changeTab () {
  const form = document.getElementById('changeTabsForm')
  const profile = document.getElementById('profile')
  const bookshelf = document.getElementById('bookshelf')
  bookshelf.classList.add('hidden')
  profile.classList.remove('hidden')
  form.onclick = (e) => {
    if (e.target.value === '1') {
      bookshelf.classList.add('hidden')
      profile.classList.remove('hidden')
    } else if (e.target.value === '2') {
      bookshelf.classList.remove('hidden')
      profile.classList.add('hidden')
    }
  }
}

function changeBackgroundOnNovePage () {
  const bg = document.querySelector('.info-bg')
  const bookImage = document.getElementById('bookImage')
  const fac = new FastAverageColor()
  fac.getColorAsync(bookImage, {
    ignoredColor: [[0, 0, 0, 255, 25], [255, 255, 255, 255, 25]]
  })
    .then(color => {
      bg.style.background = color.rgba
    })
}

function sendActivationRequest () {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
  fetch('/accounts/send_activation_email', {
    headers: {
      'X-CSRFToken': csrftoken
    }
  }).then(response => {
  })
}

function changeProfileImage () {
  const profileImg = document.getElementById('profileImg')
  const imageInput = document.getElementById('imageInput')
  const imageDemo = document.createElement('div')
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

  // eslint-disable-next-line new-cap
  const modal = new tingle.modal({
    footer: true,
    stickyFooter: false,
    closeMethods: ['overlay', 'button', 'escape'],
    closeLabel: 'Close',
    cssClass: ['custom-class-1', 'custom-class-2']
  })

  modal.addFooterBtn('Обрезать и сохранить', 'tingle-btn tingle-btn--primary', function () {
    const formData = new FormData()
    imageCrop.result('blob').then(function (image) {
      const objectURL = URL.createObjectURL(image)
      profileImg.src = objectURL
      document.getElementById('headerAccImage').src = objectURL
      formData.append('image', image)
      ajaxImagePost(formData, '/accounts/image')
    })
    modal.close()
  })

  // imageDemo is Croppie
  imageDemo.id = 'imageDemo'
  modal.setContent(imageDemo)

  profileImg.onclick = () => {
    imageInput.click()
  }

  const imageCrop = new Croppie(imageDemo, {
    viewport: {
      width: 200, height: 200, type: 'circle'
    },
    boundary: {
      width: 400, height: 400
    }
  })

  imageInput.onchange = function () {
    if (imageInput.value) {
      modal.open()
      const reader = new FileReader()
      reader.onload = function (event) {
        imageCrop.bind({
          url: event.target.result
        })
      }
      reader.readAsDataURL(this.files[0])
    }
  }

  function ajaxImagePost (data, url) {
    fetch(url, {
      method: 'POST',
      body: data,
      headers: {
        'X-CSRFToken': csrftoken
      },
      mode: 'same-origin'
    }).then(response => {
    })
  }
}

function validateEmail (email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

function setAccountEmail (block) {
  // Change link to input field on click. Send request to set email on server.
  const container = block
  const buttonChange = document.getElementById('setEmailBtn')
  const buttonConfirm = document.getElementById('emailConfirmBtn')
  const containerText = container.innerText.split('\n')[0]
  const inputField = `
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
      // eslint-disable-next-line eqeqeq
      if (input.value.trim() == '') {
        container.innerHTML = containerText
        const btnsContainer = document.createElement('div')
        btnsContainer.classList.add('profile-email__btns-container')
        // eslint-disable-next-line no-unused-expressions
        buttonChange ? btnsContainer.appendChild(buttonChange) : ''
        // eslint-disable-next-line no-unused-expressions
        buttonConfirm ? btnsContainer.appendChild(buttonConfirm) : ''
        container.appendChild(btnsContainer)
      } else {
        if (!validateEmail(input.value)) {
          return ''
        }
        container.innerHTML = '<div class="dot-pulse"></div>'
        fetch('/accounts/email_change', {
          method: 'POST',
          headers: {
            Accept: 'application/json', 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken
          },
          mode: 'same-origin',
          body: JSON.stringify({ new_email: input.value })
        })
          .then((response) => {
            if (!response.ok) {
              throw response
            }
            return response.json()
          })
          .then(resp => {
            container.innerHTML = resp.new_email
            const btnsContainer = document.createElement('div')
            btnsContainer.classList.add('profile-email__btns-container')
            btnsContainer.appendChild(buttonChange)
            btnsContainer.appendChild(buttonConfirm)
            container.appendChild(btnsContainer)
          })
          .catch(response => {
            container.innerHTML = ''
            container.appendChild(input)
            container.children[0].style.outline = '1px red solid'
            const message = document.createElement('div')
            message.innerHTML = response.message
            message.style.marginTop = '10px'
            container.appendChild(message)
          })
      }
    })
  }
}

function tagPageSorting () {
  // Sort bookCards on tag page using fetch ajax
  const form = document.getElementById('tagSort')
  const loading = document.getElementById('loading')
  const tag = document.getElementById('tag')
  form.onclick = (e) => {
    if (e.target.dataset.input === 'true') {
      loading.style.display = 'block'
      const includeTags = [tag.innerText]
      const options = {
        filters: {
          include_tags: includeTags
        },
        sort_by: e.target.value,
        pagination_options: {
          page: 1,
          books_per_page: 16
        }
      }
      renderPage(options)
        .then(() => {
          loading.style.display = 'none'
        })
    }
  }
}

function getBooksFromServer (options) {
  return fetch('/get_books_json_api/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options)
  })
    .then(response => response)
    .then(res => res.json())
}

function renderBookCards (json, whereToRender) {
  // Get list of dictionaries with book data and render it on page
  let html = ''
  for (const book of json) {
    html += createBookCard(book)
  }
  whereToRender.innerHTML = html
}

function createBookCard (novelData) {
  let tags = ''
  for (const tag of novelData.tags) {
    tags += `<a href="#" class="meta__tag bookCard__tag">${tag.name}</a>`
  }
  return `
        <div class="bookCard">
        <div class="bookCard__container">
          <div class="bookCard__column-1">
            <a href="/books/${novelData.id}" class="bookCard__image noselect">
              <img src="${novelData.book_image}" alt="book picture">
            </a>
            <div class="bookCard__buttons noselect">
              <a href="/books/${novelData.id}" class="btn bookCard__btn btn-border-anim">Читать</a>
            </div>
          </div>
          <div class="bookCard__column-2">
            <a href="/books/${novelData.id}" class="bookCard__title">${novelData.title}</a>
            ${novelData.adult_only ? '<span className="bookCard__adultOnly"> [R18+]</span>' : ''}
            <div class="bookCard__metaData">
              <a href="/authors/${novelData.author.id}" class="bookCard__author">${novelData.author.name}</a>
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

function authenticationMenu () {
  const toggleIcon = document.getElementById('accountIco')
  const dropdown = document.querySelector('.dropdown')
  document.body.onclick = (e) => {
    // if (dropdown.classList.contains('dropdown_active')) {
    //     dropdown.classList.remove('dropdown_active')
    // }
    // if (e.target.dataset)
    if (e.target.dataset.menu !== 'true') {
      dropdown.classList.remove('dropdown_active')
    }
  }
  toggleIcon.onclick = () => {
    dropdown.classList.toggle('dropdown_active')
  }
}

function catalog () {
  const loading = document.getElementById('loading')
  const includeTags = new SlimSelect({
    select: '.include-tags', searchPlaceholder: 'Поиск'
  })
  const excludeTags = new SlimSelect({
    select: '.exclude-tags', searchPlaceholder: 'Поиск'
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
    const options = {
      filters: {
        include_tags: includeTags.selected(),
        exclude_tags: excludeTags.selected(),
        chapters_more_less_select: chaptersSelect.selected(),
        chapters_number: chaptersInput.value
      },
      sort_by: sortBy.selected(),
      pagination_options: {
        page: 1,
        books_per_page: 16
      }
    }
    renderPage(options)
  }
}

function renderPage (options) {
  const placeToRender = document.getElementById('section')
  return getBooksFromServer(options)
    .then(response => {
      if (Array.isArray(response.data) && response.data.length !== 0) {
        renderBookCards(response.data, placeToRender)
      } else {
        placeToRender.innerHTML = ''
        const noFoundedMsg = document.createElement('div')
        noFoundedMsg.innerText = 'Книг не найдено'
        placeToRender.appendChild(noFoundedMsg)
      }
      renderPaginator(response.page, options)
    })
}

function BackToTop (btnClass, hideClass) {
  const btn = document.querySelector('.' + btnClass)
  if (!btn) {
    throw new Error(`Button (${btnClass}) not found`)
  } else {
    addEventListeners()
    hideBtn(btn, hideClass)
  }

  function addEventListeners () {
    document.addEventListener('scroll', () => {
      if (window.scrollY > outerHeight + outerHeight / 3) {
        showBtn(btn, hideClass)
      } else {
        hideBtn(btn, hideClass)
      }
    })
    btn.addEventListener('click', () => {
      scrollToTop()
    })
  }

  function showBtn (button, hideClass) {
    button.classList.remove(hideClass)
  }

  function hideBtn (button, hideClass) {
    button.classList.add(hideClass)
  }

  function scrollToTop () {
    const c = document.documentElement.scrollTop || document.body.scrollTop
    if (c > 0) {
      window.requestAnimationFrame(scrollToTop)
      window.scrollTo(0, c - c / 8)
    }
  }
}

function DarkMode (lightBtnClass, darkBtnClass, lightHideClass, darkHideClass) {
  const lightBtn = document.querySelector('.' + lightBtnClass)
  const darkBtn = document.querySelector('.' + darkBtnClass)
  const lightMode = window.localStorage.getItem('lightMode')
  if (lightMode === 'light') {
    document.documentElement.dataset.colorscheme = 'light'
  } else if (lightMode === 'dark') {
    document.documentElement.dataset.colorscheme = 'dark'
  } else {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      window.localStorage.setItem('lightMode', 'dark')
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      window.localStorage.setItem('lightMode', 'light')
    }
  }
  if (!lightBtn || !darkBtn) {
    throw new Error(`Can't find buttons (${lightBtnClass}, ${darkBtnClass})`)
  } else {
    if (document.documentElement.dataset.colorscheme === 'light') {
      show(darkBtn, darkHideClass)
    } else {
      show(lightBtn, lightHideClass)
    }
  }
  addEventListeners()

  function show (btn, hideClass) {
    btn.classList.remove(hideClass)
  }

  function hide (btn, hideClass) {
    btn.classList.add(hideClass)
  }

  function addEventListeners () {
    darkBtn.onclick = () => {
      hide(darkBtn, darkHideClass)
      show(lightBtn, lightHideClass)
      document.documentElement.dataset.colorscheme = 'dark'
      window.localStorage.setItem('lightMode', 'dark')
    }
    lightBtn.onclick = () => {
      hide(lightBtn, lightHideClass)
      show(darkBtn, darkHideClass)
      document.documentElement.dataset.colorscheme = 'light'
      window.localStorage.setItem('lightMode', 'light')
    }
  }
}
