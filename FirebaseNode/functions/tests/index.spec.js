const funct = require('../index.js').newImageUploaded

const event = {data:
  {
    bucket: '',
    name: '',
    contentType:'',
    resourceState:'',
    metageneration:''
  }
}

funct(event)
