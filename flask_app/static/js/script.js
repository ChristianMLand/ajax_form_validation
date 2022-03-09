const handleValidation = event => {
    event.preventDefault()
    const form = event.target

    fetch(form.action, {
        method: "POST",
        body : new FormData(form)
    })
    .then(response => response.json())
    .then(errors => {
        if (errors['message'] !== 'success') {
            for(const div of form.querySelectorAll('div')){
                for(let err of div.querySelectorAll('p')){
                    div.removeChild(err)
                }
            }
            for(const error in errors){
                const div = form.querySelector(`input[name='${error}']`).parentElement
                const alert = document.createElement('p')
                alert.classList.add('alert','alert-danger')
                alert.innerText = errors[error]
                div.append(alert)
            }
        } else {
            window.location.href = "/success"
        }
    })
}

for(const form of document.querySelectorAll("form")) {
    form.addEventListener('submit', handleValidation)
}
