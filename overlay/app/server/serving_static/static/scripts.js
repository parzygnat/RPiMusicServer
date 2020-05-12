let url = 'http://127.0.0.1:2222/files';

fetch(url, {
  method: 'GET',
  mode: 'cors'})
.then(res => res.json())
.then((out) => {
  console.log('FILESLIST! ', out);
  out.forEach(element => {
    var node = document.createElement("LI");                 // Create a <li> node
    var link = document.createElement("a");
    var linkText = document.createTextNode(element);
    link.appendChild(linkText);
    link.title = element;
    link.href = "files/" + element;  
    node.appendChild(link);                              // Append the text to <li>
    document.getElementById("list").appendChild(node);     // Append <li> to <ul> with id="myList" 
  });
})
.catch(err => { throw err });

let file_input = document.getElementById("fileInput");
function on_file_select() 
{
  if(file_input.files.length > 0) {
    let file = file_input.files[0]    // clear the data from the file input element
    file_input.value = ''
    
    if(file.size < 500000000) {
      let fd = new FormData()
      fd.append('file', file)
      axios.post('/files/' + file.name, fd, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response=> {
        var node = document.createElement("LI");                 // Create a <li> node
        var link = document.createElement("a");
        var linkText = document.createTextNode(file.name);
        link.appendChild(linkText);
        link.title = file.name;
        link.href = "files/" + file.name;  
        node.appendChild(link);                              // Append the text to <li>
        document.getElementById("list").appendChild(node);
      })
      .catch(err=> {
        // handle error
      })
    } else {
       // show an error
    }
  }
}

file_input.addEventListener('change', on_file_select);
