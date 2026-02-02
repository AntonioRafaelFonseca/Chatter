const messageList = document.querySelector('#messagesList')
const inputSel = document.querySelector('#inputSel')
const btn = document.querySelector('#btn');

clearDatabase()

function showMessages()
{
  getMsgs()
  .then(msgs => {
    messageList.innerHTML = '';

    msgs.forEach(msg => {
        const item = document.createElement('li')
        item.textContent = msg 
        messageList.appendChild(item)      
    });
    messageList.scrollTop = messageList.scrollHeight;
  })
}

async function getMsgs() {
  const res = await fetch('/messages')
  const data = await res.json()
  return data
}


function addMsg(intended)
{
  if(!intended) return
  fetch('/messages', {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({content: intended})
  })
  .then(() => {console.log(`added ${intended} to database`);showMessages()})
  .catch(err => console.log(err))
  
}

function clearDatabase()
{
  fetch('/messages', {method: 'DELETE'})

  .then(() => {console.log('deleted database')
    showMessages()
  })
}

function GetInput() {
  const val = inputSel.value.trim()
  inputSel.value = ''
  return val || null
}

btn.addEventListener('click', () => {
  addMsg(GetInput())
})
document.addEventListener('keydown', e => {
  if (e.key == 'Enter'){
    addMsg(GetInput())
  }
})

// document.addEventListener('keydown', clearDatabase)