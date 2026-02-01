const messageList = document.querySelector('#messagesList')
const inputSel = document.querySelector('#inputSel')
const btn = document.querySelector('#btn')

function showMessages() {
  getMsgs().then(msgs => {
    messageList.innerHTML = ''

    msgs.forEach(msg => {
      const item = document.createElement('li')
      item.textContent = msg
      messageList.appendChild(item)
    })

    // 🔽 auto-scroll
    messageList.scrollTop = messageList.scrollHeight
  })
}

async function getMsgs() {
  const res = await fetch('/messages')
  return await res.json()
}

function addMsg(text) {
  if (!text) return

  fetch('/messages', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ content: text })
  })
  .then(showMessages)
}

function GetInput() {
  const val = inputSel.value.trim()
  inputSel.value = ''
  return val
}

btn.addEventListener('click', () => {
  addMsg(GetInput())
})

document.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    addMsg(GetInput())
  }
})

showMessages()
