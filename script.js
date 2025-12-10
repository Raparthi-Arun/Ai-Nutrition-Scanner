/************************
 * NutriScan Frontend
 * - Handles file upload & camera capture
 * - Shows preview, fake API call, and result UI
 ************************/

const API_ENDPOINT = "http://localhost:8000/api/scans/process_image/";

// Elements
const preview = document.getElementById('preview');
const previewImg = document.getElementById('previewImg');
const cameraFeed = document.getElementById('cameraFeed');
const fileInput = document.getElementById('fileInput');
const captureBtn = document.getElementById('captureBtn');
const startCamBtn = document.getElementById('startCamBtn');
const stopCamBtn = document.getElementById('stopCamBtn');
const clearBtn = document.getElementById('clearBtn');
const exampleBtn = document.getElementById('exampleBtn');
const statusText = document.getElementById('statusText');
const statusIcon = document.getElementById('statusIcon');

const calText = document.getElementById('calText');
const proteinText = document.getElementById('proteinText');
const carbText = document.getElementById('carbText');
const fatText = document.getElementById('fatText');
const proteinFill = document.getElementById('proteinFill');
const carbFill = document.getElementById('carbFill');
const fatFill = document.getElementById('fatFill');
const portionText = document.getElementById('portionText');
const confText = document.getElementById('confText');

const historyList = document.getElementById('historyList');

let currentBlob = null;
let streamRef = null;

// Helpers
function setStatus(text, busy=false){
  statusText.textContent = text;
  statusIcon.innerHTML = busy ? '<div class="loader"></div>' : '';
}

function setPreviewImage(url){
  previewImg.src = url;
  previewImg.style.display = 'block';
  cameraFeed.style.display='none';

  const hint = preview.querySelector('.drop-hint');
  if(hint) hint.style.display='none';
}

function clearPreview(){
  previewImg.src = '';
  previewImg.style.display='none';
  cameraFeed.style.display='none';

  const hint = preview.querySelector('.drop-hint');
  if(hint) hint.style.display='block';

  currentBlob = null;
}

function dataURLToBlob(dataURL){
  const parts = dataURL.split(',');
  const mime = parts[0].match(/:(.*?);/)[1];
  const binStr = atob(parts[1]);
  const arr = new Uint8Array(binStr.length);
  for(let i=0;i<binStr.length;i++) arr[i]=binStr.charCodeAt(i);
  return new Blob([arr], {type:mime});
}

// Drag & Drop
preview.addEventListener('dragover', e => {
  e.preventDefault(); 
  preview.style.borderColor = 'rgba(255,255,255,0.12)';
});
preview.addEventListener('dragleave', () => preview.style.borderColor = 'transparent');
preview.addEventListener('drop', e => {
  e.preventDefault();
  preview.style.borderColor = 'transparent';
  const f = e.dataTransfer.files[0];
  if(f) handleFile(f);
});

// File picker
fileInput.addEventListener('change', e => {
  const f = e.target.files[0];
  if(f) handleFile(f);
});

function handleFile(file){
  if(!file.type.startsWith('image/')) return alert('Please upload an image.');
  const url = URL.createObjectURL(file);
  setPreviewImage(url);
  currentBlob = file;
  setStatus('Image ready');
}

// Example image
exampleBtn.addEventListener('click', ()=>{
  const c = document.createElement('canvas'); 
  c.width=800; c.height=600;
  const ctx = c.getContext('2d');
  ctx.fillStyle='#f6f6f8'; ctx.fillRect(0,0,c.width,c.height);
  ctx.fillStyle='#fff7cc'; ctx.beginPath(); ctx.arc(400,300,180,0,Math.PI*2); ctx.fill();
  ctx.fillStyle='#ff9e9e'; ctx.fillRect(280,250,220,80);

  const url = c.toDataURL('image/jpeg',0.9);
  setPreviewImage(url);
  currentBlob = dataURLToBlob(url);
  setStatus('Example loaded');
});

// Camera
startCamBtn.addEventListener('click', async ()=>{
  try{
    if(streamRef) return;
    const stream = await navigator.mediaDevices.getUserMedia({
      video:{facingMode:'environment',width:{ideal:1280}}, 
      audio:false
    });

    streamRef = stream;
    cameraFeed.srcObject = stream;
    cameraFeed.style.display='block';
    previewImg.style.display='none';
    setStatus('Camera active');
  }catch(err){
    alert('Camera not available or permission denied.');
  }
});

stopCamBtn.addEventListener('click', ()=>{
  if(streamRef){
    streamRef.getTracks().forEach(t=>t.stop());
    streamRef=null;
  }
  cameraFeed.style.display='none';
  setStatus('Camera stopped');
});

async function captureFromCamera(){
  if(!streamRef) return alert('Start camera first.');
  const video = cameraFeed;
  const c=document.createElement('canvas');
  c.width=video.videoWidth;
  c.height=video.videoHeight;
  c.getContext('2d').drawImage(video,0,0);
  const dataURL = c.toDataURL('image/jpeg',0.88);
  currentBlob = dataURLToBlob(dataURL);
  setPreviewImage(dataURL);
}

// Scan
captureBtn.addEventListener('click', async ()=>{
  setStatus('Processing...', true);

  if(streamRef && (!currentBlob || previewImg.style.display==='none')){
    await captureFromCamera();
  }
  if(!currentBlob) return alert('Please upload or capture an image first.');

  await fakeSendToBackend(currentBlob);
});

// Clear
clearBtn.addEventListener('click', ()=>{
  clearPreview();
  setStatus('Cleared');
});

// Send to Django backend
async function fakeSendToBackend(blob){
  setStatus('Analyzing image...', true);
  
  try {
    console.log('Sending image to:', API_ENDPOINT);
    const formData = new FormData();
    // Use original filename if available, otherwise use blob name
    const filename = blob.name || 'image.jpg';
    formData.append('image', blob, filename);
    // Also send original filename as a separate field for backend to use
    formData.append('original_filename', filename);
    
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
      }
    });
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      let errorData = {};
      try {
        errorData = await response.json();
      } catch (e) {
        errorData = { error: response.statusText };
      }
      throw new Error(errorData.error || `HTTP Error: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('Result:', result);
    
    updateResults({
      calories: result.calories,
      protein: result.protein,
      carbs: result.carbs,
      fat: result.fat,
      confidence: result.confidence,
      portion: result.portion_size
    });
    
    // Add to history with API response
    const url = URL.createObjectURL(blob);
    addHistory({
      url,
      calories: result.calories,
      protein: result.protein,
      carbs: result.carbs,
      fat: result.fat,
      confidence: result.confidence,
      foodItem: result.food_item,
      scanId: result.id
    });
    
    setStatus('Analysis complete');
    
  } catch (error) {
    console.error('Backend error:', error);
    alert(`Error: ${error.message}\n\nMake sure Django backend is running at ${API_ENDPOINT}`);
    setStatus('Error analyzing image');
  }
}

function updateResults({calories,protein,carbs,fat,confidence,portion}){
  calText.textContent = calories + ' kcal';
  proteinText.textContent = protein + ' g';
  carbText.textContent = carbs + ' g';
  fatText.textContent = fat + ' g';
  portionText.textContent = portion;
  confText.textContent = confidence + ' %';

  proteinFill.style.width = Math.min(100, (protein/60)*100) + '%';
  carbFill.style.width = Math.min(100, (carbs/120)*100) + '%';
  fatFill.style.width = Math.min(100, (fat/60)*100) + '%';
}

function addHistory(item){
  const div = document.createElement('div');
  div.className='history-item';

  const foodLabel = item.foodItem ? `${item.foodItem} • ` : '';

  div.innerHTML = `
    <img src="${item.url}" alt="scan" />
    <div class="history-info">
      <p>${foodLabel}${item.calories.toFixed(0)} kcal</p>
      <small>Confidence: ${item.confidence.toFixed(0)}% • P: ${item.protein.toFixed(1)}g • C: ${item.carbs.toFixed(1)}g • F: ${item.fat.toFixed(1)}g</small>
    </div>`;

  historyList.prepend(div);
}
