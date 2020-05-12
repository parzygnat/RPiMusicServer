let url = 'http://127.0.0.1:2222/files';
let num = 1
fetch(url, {
  method: 'GET',
  mode: 'cors'})
.then(res => res.json())
.then((out) => {
  console.log('FILESLIST! ', out);
  out.forEach(element => {
    var node = document.createElement("p");                 // Create a <li> node
    var link = document.createElement("a");
    var linkText = document.createTextNode( element);
    link.appendChild(linkText);
    link.title = element;
    num++;
    link.href = "files/" + element;  
    link.addEventListener('contextmenu', function(elem) {  
      elem.preventDefault()
      elem = elem.target
      let queue = document.getElementById("list").childNodes
      let parent = document.getElementById("list");
      let ugh = Array.prototype.indexOf.call(parent.children, elem.parentNode);
      console.log(ugh)
      if(ugh != 0) {
        swapElements(queue[ugh], queue[ugh + 1]);
        generateJSON(queue)
      }
    })  
    link.addEventListener('mousedown', function(elem) {  
      if(elem.button == 1) {
        elem.preventDefault();
        let ugh2 = Array.prototype.indexOf.call(document.getElementById("list").children, elem.target.parentNode);
        console.log(ugh2)
        axios.delete('/delete/' + ugh2, {
          data: {
            num: ugh2
          }
        });
        let queue = document.getElementById("list").removeChild(elem.target.parentNode)
      }
    })
    node.appendChild(link);        
      // Append the text to <li>
    document.getElementById("list").appendChild(node); 
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
        var node = document.createElement("p");                 // Create a <li> node
        var link = document.createElement("a");
        var linkText = document.createTextNode( file.name);
        link.appendChild(linkText);
        link.title = file.name;
        num++;
        link.href = "files/" + file.name;  
        link.addEventListener('contextmenu', function(elem) {  
          elem.preventDefault()
          elem = elem.target
          let queue = document.getElementById("list").childNodes
          let parent = document.getElementById("list");
          let ugh = Array.prototype.indexOf.call(parent.children, elem.parentNode);
          console.log(ugh)
          if(ugh != 0) {
            swapElements(queue[ugh], queue[ugh + 1]);
            generateJSON(queue)
          }
        }) 
        link.addEventListener('mousedown', function(elem) {  
          if(elem.button == 1) {
            elem.preventDefault();
            let ugh2 = Array.prototype.indexOf.call(document.getElementById("list").children, elem.target.parentNode);
            console.log(ugh2)
            axios.delete('/delete/' + ugh2, {
              data: {
                num: ugh2
              }
            });
            let queue = document.getElementById("list").removeChild(elem.target.parentNode)
          }
        })   
        node.appendChild(link);        
          // Append the text to <li>
        document.getElementById("list").appendChild(node); 
      })
      .catch(err=> {
        console.log(err);
      })
    } else {
       console.log('else');
    }
  }
}

function rightClick(elem) {

}

file_input.addEventListener('change', on_file_select);

function swapElements(obj1, obj2) {
  // create marker element and insert it where obj1 is
  var temp = document.createElement("div");
  obj1.parentNode.insertBefore(temp, obj1);

  // move obj1 to right before obj2
  obj2.parentNode.insertBefore(obj1, obj2);

  // move obj2 to right before where obj1 used to be
  temp.parentNode.insertBefore(obj2, temp);

  // remove temporary marker node
  temp.parentNode.removeChild(temp);
}

function generateJSON(arg1) {
  console.log(arg1)
  final = [];
  const [, ...rest] = arg1;
  rest.forEach(element => {
    final.push(element.childNodes[0].textContent)
  });
  axios.post('/update', final);
}