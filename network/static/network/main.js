document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#submit-post').addEventListener('click', create_post());
    
    load_posts();
});

async function load_posts() {
    const posts = document.querySelector('#posts');
    await fetch('/network/posts')
    .then(response => response.json())
    .then(data => {
        data.forEach(post => {
            const div = document.createElement('div');
            div.innerHTML = post.content;
            div.className = 'post';
            posts.appendChild(div);
        })
    })
    await fetch('/posts', {
        method: 'GET',
        body: JSON.stringify({
            content: content
        })
    })
}

async function create_post() {
    const content = document.querySelector('#post-content').value;
    await fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    })

    load_posts();
}