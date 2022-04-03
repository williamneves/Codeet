// Add new Codeet Dynamically

function submit_new_codeet(input_data) {

    data = {
        'text': input_data.target.text.value,
        'user_id': input_data.target.user_id.value,
    }

    let text_codeet = document.getElementById('post-tweet-text')
    text_codeet.disabled = true;


    let btn = document.querySelector("#btn-post-codeet-profile")
    let originalInnerHtml = btn.innerHTML
    btn.innerHTML = `<button class="btn btn-primary m-0 align-self-center me-1"style="width:110px;" disabled>Posting...<i class="fas fa-spinner fa-spin"></i></button>`
    let card = document.getElementById('new-codeet-card')

    axios.post('/add-codeet/', data)
        .then(response => {

            setTimeout(() => {
                btn.innerHTML = originalInnerHtml
            }, 2000)
            setTimeout(() => {


                text_codeet.disabled = false;
                text_codeet.value = ""

                let newCodeet = createCodeet(response.data)
                document.getElementById('dynamic-codeet').prepend(newCodeet)
            }, 3000)

            setTimeout(() => {
                let card = document.getElementById('new-codeet-card')
                card.classList.remove("border-warning")
            }, 15000)

        })
        .catch(error => {
            console.log(error)
        })
}

function createCodeet(data) {
    console.log(data)
    let codeet = document.createElement("div")
    codeet.innerHTML = data
    codeet.classList.add("new-box")
    codeet.classList.add("border-warning")
    return codeet
}

// NEW LIKE
function submit_new_like(like) {

    data = {
        'codeet_id': like.target.codeet_id.value,
        'user_id': like.target.user_id.value,
    }

    //Selecting the button like by id and codeet id
    let like_btn = document.querySelector(`#like-codeet-btn-${data['codeet_id']}`)

    // If the user has NOT liked the codeet
    if (!like_btn.classList.contains('codeet-liked')) {

        like_btn.disabled = true;

        console.log('liking')

        axios.post('/add-like/', data)
            .then(res => {
                // show response
                console.log(res)
                // reactivate button in 5 second -> setTimeout
                setTimeout(() => {
                    like_btn.classList.add("text-primary")
                    like_btn.classList.add("codeet-liked")
                    like_btn.classList.remove("text-secondary")
                }, 700)
                setTimeout(() => {
                    like_btn.disabled = false;
                }, 5000)

            })
            .catch(error => {
                console.log(error)
            })

    }

    // If the user HAS liked the codeet
    else {
        like_btn.disabled = true;

        console.log('unliking')

        axios.post('/add-like/', data)
            .then(res => {
                // show response
                console.log(res)
                // reactivate button in 5 second -> setTimeout
                setTimeout(() => {
                    like_btn.classList.remove("text-primary")
                    like_btn.classList.remove("codeet-liked")
                    like_btn.classList.add("text-secondary")
                }, 700)

                setTimeout(() => {
                    like_btn.disabled = false;
                }, 5000)

            })
            .catch(error => {
                console.log(error)
            })

    }

}