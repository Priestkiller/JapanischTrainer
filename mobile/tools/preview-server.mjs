import http from 'node:http';
import {readFileSync,existsSync,statSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const mime={'.html':'text/html; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.txt':'text/plain; charset=utf-8'};
export function previewServer(port=0) {
 const server=http.createServer((req,res)=>{
  try {
   const relative=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\/+/, '')||'index.html';
   if(relative.includes('..')||relative.includes('\\'))throw Error('Invalid path');
   const file=[path.join(root,'web',relative),path.join(root,'generated/assets',relative)].find(f=>existsSync(f)&&statSync(f).isFile());
   if(!file){res.writeHead(404);res.end('Not found');return;}
   res.writeHead(200,{'Content-Type':mime[path.extname(file)]??'application/octet-stream','Cache-Control':'no-store'});res.end(readFileSync(file));
  }catch(e){res.writeHead(400);res.end('Invalid request');}
 });
 return new Promise(resolve=>server.listen(port,'127.0.0.1',()=>resolve(server)));
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 const server=await previewServer(Number(process.env.PORT??8765));console.log(`http://127.0.0.1:${server.address().port}`);
}
