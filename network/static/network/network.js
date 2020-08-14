document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelector("#post").addEventListener('click', SubmitPost)


});

function SubmitPost() {
    content = document.querySelector("#id_Content").value;
    fetch(`/postnew`, {
        method: 'POST',
        body: JSON.stringify({
            Content: content,
        })
    })
    content = "";
}

function EditPost(PostID) {
    fetch(`/EditPost`, {
        method: "PUT",
        body: JSON.stringify({
            id: PostID,
        })
    })
    .then(response => response.json())
    .then(result => {
        
        const element = document.createElement("textarea");
        element.value = result;
        element.id = "Edited";
        const save = document.createElement("input");
        save.type = "submit"
        save.addEventListener('click', function(x) {
            SavePost(PostID)
            x.preventDefault();
        }, false);
        save.addEventListener('click', function(a) {
            x = document.getElementById("Edited").value;
            document.getElementById(`${PostID}`).innerHTML = x
            a.preventDefault();
        }, false);
        document.getElementById(`${PostID}`).append(save);
        document.getElementById(`${PostID}`).append(element);
        document.getElementById(`${PostID}text`).innerHTML = ``
        
         })
    return false        
    
}
function SavePost(ID) {
    x = document.getElementById("Edited").value;
    fetch(`/EditPost`, {
        method: 'POST',
        body: JSON.stringify({
            Content: x,
            id: ID,
        })
    })
    return false 
    
}

function Like(postid, userid){
    fetch("/Likes", {
        method: "POST",
        body: JSON.stringify({
            postid: postid,
            userid: userid,
        })
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById(`${postid}Like`).innerHTML = result
    CountLike(postid)})

}
function CountLike(postid){

    fetch("/getLikeCount", {
        method: "POST",
        body: JSON.stringify({
            postid: postid,
        })
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById(`like${postid}`).innerHTML = result
        
    }) 

}