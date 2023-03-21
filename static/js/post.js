const post_content = document.querySelector('#post_content');

post_content.innerHTML = post_content.innerHTML.replaceAll("#code#","<pre><code>");
post_content.innerHTML = post_content.innerHTML.replaceAll("#/code#","</code></pre>");
post_content.innerHTML = post_content.innerHTML.replaceAll("#b#","<b>");
post_content.innerHTML = post_content.innerHTML.replaceAll("#/b#","</b>");
post_content.innerHTML = post_content.innerHTML.replaceAll("#strong#","<strong>");
post_content.innerHTML = post_content.innerHTML.replaceAll("#/strong#","</strong>");
const all_img_elements = post_content.innerHTML.match(/#img#.*?#\/img#/g);
try{
  all_img_elements.forEach((value)=>{
  let element_item = value.split("#");
  let id = element_item[2];
  const new_img = `<img class="cover-img" src="https://drive.google.com/thumbnail?id=${id}" alt=""/>`
  post_content.innerHTML = post_content.innerHTML.replaceAll("#img#"," ");
  post_content.innerHTML = post_content.innerHTML.replaceAll("#/img#"," ");
  post_content.innerHTML = post_content.innerHTML.replace(id, new_img);
})

}
catch(e) {
  console.error(e);
}


try {
  document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('pre code').forEach((el) => {
    hljs.highlightElement(el);
  });
});
}
catch(e) {
  console.error(e)
}
