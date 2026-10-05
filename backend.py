<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Emvic Clipper PRO — Multi-Format AI Video Studio</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts: Plus Jakarta Sans & Space Grotesk -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            display: ['"Space Grotesk"', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              400: '#818cf8',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
            }
          }
        }
      }
    }
  </script>
  <style>
    .aspect-9-16 { aspect-ratio: 9 / 16; }
    .aspect-1-1 { aspect-ratio: 1 / 1; }
    .aspect-16-9 { aspect-ratio: 16 / 9; }

    .glass-panel {
      background: rgba(15, 23, 42, 0.78);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .phone-mockup-frame {
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 0 8px #1e293b, 0 0 0 10px #334155;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .monitor-mockup-frame {
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 0 6px #1e293b, 0 0 0 8px #334155;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .custom-scroll::-webkit-scrollbar { width: 5px; height: 5px; }
    .custom-scroll::-webkit-scrollbar-track { background: transparent; }
    .custom-scroll::-webkit-scrollbar-thumb { background: #334155; border-radius: 9999px; }
    .custom-scroll::-webkit-scrollbar-thumb:hover { background: #475569; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-brand-500 selection:text-white pb-12">
  
  <!-- Subtle Ambient Glows -->
  <div class="fixed top-0 left-1/4 w-[32rem] h-[32rem] bg-brand-600/10 rounded-full blur-3xl pointer-events-none -z-10"></div>
  <div class="fixed bottom-0 right-1/4 w-[32rem] h-[32rem] bg-indigo-500/10 rounded-full blur-3xl pointer-events-none -z-10"></div>

  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
    
    <!-- Top Brand & Meta Navigation -->
    <header class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-800/80 mb-8">
      <div class="flex items-center gap-3.5">
        <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-brand-600 via-indigo-500 to-sky-400 flex items-center justify-center shadow-lg shadow-brand-500/30">
          <span class="text-2xl">⚡</span>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-2xl font-extrabold text-white tracking-tight font-display">Emvic Clipper</h1>
            <span class="text-[10px] bg-gradient-to-r from-brand-500 to-indigo-500 text-white font-extrabold px-2 py-0.5 rounded-full shadow-sm">PRO</span>
          </div>
          <p class="text-xs text-slate-400 mt-0.5">Autonomous AI Clip Extraction & Multi-Aspect Cropper</p>
        </div>
      </div>
      
      <div class="flex flex-wrap items-center gap-3">
        <div class="flex items-center gap-2 text-xs bg-slate-900/90 border border-slate-800 px-3.5 py-1.5 rounded-full text-slate-300 font-medium">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Groq Whisper Large-v3</span>
        </div>
        <div id="activeAspectPill" class="text-xs bg-indigo-950/80 border border-indigo-700/60 px-3.5 py-1.5 rounded-full text-indigo-300 font-semibold shadow-inner flex items-center gap-1.5">
          <span id="pillIcon">📱</span>
          <span id="pillText">9:16 Vertical FHD</span>
        </div>
      </div>
    </header>

    <main class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      
      <!-- LEFT CONFIGURATION CONSOLE (5 Cols) -->
      <section class="lg:col-span-5 space-y-5">
        <div class="glass-panel rounded-3xl p-6 shadow-2xl space-y-5 border border-slate-800/80">
          
          <div class="flex items-center justify-between border-b border-slate-800/80 pb-4">
            <div>
              <h2 class="text-base font-bold text-white flex items-center gap-2 font-display">
                <span>🎛</span> Ingestion Console
              </h2>
              <p class="text-xs text-slate-400 mt-0.5">Customize your framing, duration & output source.</p>
            </div>
            <span class="text-[11px] font-mono text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded-md font-semibold">
              FFmpeg Ready
            </span>
          </div>

          <!-- YouTube URL Input -->
          <div class="space-y-1.5">
            <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider">Source YouTube Video</label>
            <div class="relative flex items-center">
              <span class="absolute left-3.5 pointer-events-none text-slate-500 text-sm">▶</span>
              <input id="youtubeUrl" type="text" placeholder="https://www.youtube.com/watch?v=..." class="w-full bg-slate-900 border border-slate-700/80 rounded-xl pl-9 pr-16 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition shadow-inner">
              <button type="button" onclick="pasteClipboard()" class="absolute right-2 text-xs font-semibold text-brand-400 hover:text-white bg-slate-800 hover:bg-slate-700 px-2.5 py-1.5 rounded-lg border border-slate-700 transition">
                Paste
              </button>
            </div>
          </div>

          <!-- Clip Naming Prefix -->
          <div class="space-y-1.5">
            <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider">Clip Naming Prefix</label>
            <input id="customName" type="text" placeholder="e.g. DiaryOfACE0_Ep42" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition shadow-inner">
          </div>

          <!-- DYNAMIC MULTI-ASPECT RATIO SELECTOR -->
          <div class="space-y-2 pt-1">
            <div class="flex items-center justify-between">
              <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider">Output Framing / Aspect Ratio</label>
              <span class="text-[11px] text-slate-400 font-mono" id="resolutionTag">1080 × 1920 (FHD)</span>
            </div>
            
            <div class="grid grid-cols-3 gap-2.5">
              <!-- 9:16 Vertical -->
              <button type="button" onclick="setAspectRatio('9:16', '1080x1920', '📱 9:16 Vertical FHD', 'Shorts / Reels / TikTok', this)" class="aspect-btn active-aspect group relative p-3 rounded-2xl border text-left transition flex flex-col justify-between bg-brand-950/40 border-brand-500 text-white shadow-lg shadow-brand-500/10">
                <div class="flex items-center justify-between">
                  <span class="text-lg">📱</span>
                  <span class="text-[10px] font-mono font-bold bg-brand-500/20 text-brand-300 px-1.5 py-0.5 rounded">9:16</span>
                </div>
                <div class="mt-2">
                  <div class="text-xs font-bold leading-tight">Vertical</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Shorts / Reels</div>
                </div>
              </button>

              <!-- 1:1 Square -->
              <button type="button" onclick="setAspectRatio('1:1', '1080x1080', '🟦 1:1 Square Feed', 'Instagram / LinkedIn Feed', this)" class="aspect-btn group relative p-3 rounded-2xl border text-left transition flex flex-col justify-between bg-slate-900/90 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white">
                <div class="flex items-center justify-between">
                  <span class="text-lg">🟦</span>
                  <span class="text-[10px] font-mono font-bold bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">1:1</span>
                </div>
                <div class="mt-2">
                  <div class="text-xs font-bold leading-tight">Square</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Post Feed</div>
                </div>
              </button>

              <!-- 16:9 Landscape -->
              <button type="button" onclick="setAspectRatio('16:9', '1920x1080', '🖥 16:9 Landscape HD', 'YouTube / Desktop Web', this)" class="aspect-btn group relative p-3 rounded-2xl border text-left transition flex flex-col justify-between bg-slate-900/90 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white">
                <div class="flex items-center justify-between">
                  <span class="text-lg">🖥</span>
                  <span class="text-[10px] font-mono font-bold bg-slate-800 text-slate-400 px-1.5 py-0.5 rounded">16:9</span>
                </div>
                <div class="mt-2">
                  <div class="text-xs font-bold leading-tight">Landscape</div>
                  <div class="text-[10px] text-slate-400 mt-0.5">Wide Stream</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Target Hook Duration Preset Selector -->
          <div class="space-y-2 pt-1">
            <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider">Hook Duration Target</label>
            <div class="grid grid-cols-3 gap-2">
              <button type="button" onclick="setDurationTarget(60, 90, this)" class="dur-btn p-2.5 rounded-xl border bg-slate-900/90 border-slate-800 text-slate-300 hover:border-slate-700 text-center transition">
                <div class="text-xs font-bold">60s — 90s</div>
                <div class="text-[10px] text-slate-400">Sweet Spot</div>
              </button>
              <button type="button" onclick="setDurationTarget(90, 120, this)" class="dur-btn p-2.5 rounded-xl border bg-brand-950/40 border-brand-500 text-white text-center transition shadow-sm">
                <div class="text-xs font-bold">90s — 120s</div>
                <div class="text-[10px] text-slate-400">Deep Dive</div>
              </button>
              <button type="button" onclick="setDurationTarget(30, 60, this)" class="dur-btn p-2.5 rounded-xl border bg-slate-900/90 border-slate-800 text-slate-300 hover:border-slate-700 text-center transition">
                <div class="text-xs font-bold">30s — 60s</div>
                <div class="text-[10px] text-slate-400">Fast Paced</div>
              </button>
            </div>
          </div>

          <!-- Clip Count Slider -->
          <div class="space-y-2 pt-2 border-t border-slate-800/80">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-300 uppercase tracking-wider">Number of Clips</span>
              <span id="clipCountLabel" class="bg-brand-600/30 text-brand-300 border border-brand-500/30 font-bold px-2.5 py-0.5 rounded-md font-mono">3 Viral Shorts</span>
            </div>
            <input id="numClips" type="range" min="1" max="8" value="3" oninput="clipCountLabel.innerText = this.value + ' Viral Shorts'" class="w-full accent-brand-500 cursor-pointer">
            <div class="flex justify-between text-[11px] text-slate-500 font-mono">
              <span>1</span>
              <span>3</span>
              <span>5</span>
              <span>8</span>
            </div>
          </div>

          <!-- Optional Groq Key Accordion -->
          <details class="group pt-2 border-t border-slate-800/80">
            <summary class="flex items-center justify-between text-xs font-bold text-slate-400 cursor-pointer hover:text-slate-200 select-none">
              <span>Advanced API Credentials</span>
              <span class="text-xs text-brand-400 group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <div class="mt-3 space-y-1">
              <input id="groqKey" type="password" placeholder="Custom Groq API Key (Optional)" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-brand-500 transition shadow-inner">
              <p class="text-[10px] text-slate-500">Leave blank to use pre-configured environment credentials.</p>
            </div>
          </details>

          <!-- Submit Button -->
          <button id="generateBtn" onclick="startGeneration()" class="w-full bg-gradient-to-r from-brand-600 via-indigo-600 to-brand-500 hover:from-brand-500 hover:to-indigo-500 active:scale-[0.99] text-white font-extrabold py-4 rounded-2xl transition duration-150 shadow-xl shadow-brand-600/25 flex items-center justify-center gap-2 cursor-pointer">
            <span>⚡ Generate Viral Clips with Emvic</span>
          </button>
        </div>

        <!-- Live Pipeline Monitor Card -->
        <div id="statusContainer" class="hidden glass-panel rounded-3xl p-5 shadow-2xl border-l-4 border-l-brand-500 space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <svg id="spinner" class="animate-spin h-4 w-4 text-brand-400" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <span id="stageLabel" class="text-xs font-extrabold uppercase tracking-wider text-brand-400 font-display">Processing Pipeline</span>
            </div>
            <span id="jobTimer" class="text-[11px] font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">In Progress</span>
          </div>

          <p id="statusStep" class="text-xs text-slate-200 font-medium">Initializing job parameters...</p>

          <!-- Stepper Visualizer -->
          <div class="grid grid-cols-3 gap-1.5 pt-2">
            <div id="stepDot1" class="h-1.5 rounded-full bg-brand-500 transition-colors"></div>
            <div id="stepDot2" class="h-1.5 rounded-full bg-slate-800 transition-colors"></div>
            <div id="stepDot3" class="h-1.5 rounded-full bg-slate-800 transition-colors"></div>
          </div>

          <div id="errorAlert" class="hidden p-3 bg-red-950/80 border border-red-800 text-red-300 text-xs rounded-xl font-mono break-words"></div>
        </div>
      </section>

      <!-- RIGHT PREVIEW & GALLERY SECTION (7 Cols) -->
      <section class="lg:col-span-7 space-y-6">
        
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-xl">📱</span>
            <h2 class="text-base font-bold text-white font-display">Device Preview & Outputs</h2>
          </div>
          <span id="exportedCountTag" class="text-xs text-slate-400 font-mono">0 Clips Exported</span>
        </div>

        <!-- Dynamic Device Mockup Canvas -->
        <div class="glass-panel rounded-3xl p-6 sm:p-8 flex flex-col items-center justify-center min-h-[560px] relative overflow-hidden border border-slate-800/80 shadow-2xl">
          
          <!-- Selected Clip Info Bar (Top overlay) -->
          <div id="activeClipBar" class="hidden w-full max-w-md mb-4 bg-slate-900/90 border border-slate-800 px-4 py-2.5 rounded-xl flex items-center justify-between text-xs">
            <div class="flex items-center gap-2 truncate">
              <span class="text-brand-400 font-bold">▶ Playing:</span>
              <span id="activeClipTitle" class="text-slate-200 font-medium truncate max-w-[200px]">Clip 1</span>
            </div>
            <span id="activeClipAspectBadge" class="bg-indigo-950 text-indigo-300 border border-indigo-800 px-2 py-0.5 rounded font-mono text-[10px]">9:16 FHD</span>
          </div>

          <!-- THE ADAPTIVE VIEWPORT FRAME -->
          <div id="viewportContainer" class="phone-mockup-frame relative bg-black rounded-[42px] overflow-hidden w-full max-w-[290px] aspect-9-16 flex items-center justify-center border-4 border-slate-900 transition-all duration-300">
            
            <!-- Dynamic Island / Speaker Notch (Visible in 9:16 mode) -->
            <div id="notchHeader" class="absolute top-2.5 z-20 w-24 h-4 bg-black rounded-full flex items-center justify-between px-2.5">
              <span class="w-1.5 h-1.5 rounded-full bg-slate-800"></span>
              <span class="w-2 h-2 rounded-full bg-emerald-500/80 animate-pulse"></span>
            </div>

            <!-- Video Player Element -->
            <video id="previewPlayer" controls playsinline class="w-full h-full object-cover hidden z-10"></video>

            <!-- Blank Slate Empty State -->
            <div id="previewPlaceholder" class="p-8 text-center flex flex-col items-center justify-center text-slate-500 space-y-3">
              <div class="w-14 h-14 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-center text-2xl shadow-inner">
                <span id="frameIcon">📱</span>
              </div>
              <div>
                <p id="frameTitle" class="text-xs font-bold text-slate-300 font-display">Device Viewport Ready</p>
                <p id="frameSubtitle" class="text-[11px] text-slate-500 mt-1 max-w-[200px]">Rendered clips preview here automatically with accurate aspect ratios.</p>
              </div>
            </div>
          </div>

          <!-- Bottom Control Strip for Active Preview -->
          <div id="previewActions" class="hidden mt-6 flex flex-wrap items-center justify-center gap-3">
            <a id="downloadActiveBtn" href="#" download="clip.mp4" class="bg-brand-600 hover:bg-brand-500 active:scale-[0.98] text-white text-xs font-bold px-4 py-2.5 rounded-xl shadow-lg shadow-brand-600/30 flex items-center gap-2 transition">
              <span>⬇</span>
              <span>Download Active Clip</span>
            </a>
            <button type="button" onclick="copyCurrentClipLink()" class="bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-semibold px-4 py-2.5 rounded-xl border border-slate-700 transition flex items-center gap-1.5">
              <span>📋</span>
              <span id="copyLinkText">Copy Video Link</span>
            </button>
          </div>
        </div>

        <!-- Clips Collection Grid -->
        <div id="gallerySection" class="hidden space-y-3">
          <h3 class="text-sm font-bold text-white uppercase tracking-wider font-display flex items-center gap-2">
            <span>🗂</span> Extracted Clips Collection
          </h3>
          <div id="clipsGrid" class="grid grid-cols-1 sm:grid-cols-2 gap-4"></div>
        </div>

      </section>

    </main>
  </div>

  <script>
    // State variables
    let currentAspectRatio = '9:16';
    let currentResolution = '1080x1920';
    let minDuration = 90;
    let maxDuration = 120;
    let pollInterval = null;
    let currentClipUrl = '';

    // Switch between 9:16, 1:1, and 16:9
    function setAspectRatio(ratio, resolution, pillText, desc, btnEl) {
      currentAspectRatio = ratio;
      currentResolution = resolution;

      // Update active button highlights
      document.querySelectorAll('.aspect-btn').forEach(btn => {
        btn.classList.remove('active-aspect', 'bg-brand-950/40', 'border-brand-500', 'text-white', 'shadow-lg');
        btn.classList.add('bg-slate-900/90', 'border-slate-800', 'text-slate-300');
      });
      btnEl.classList.add('active-aspect', 'bg-brand-950/40', 'border-brand-500', 'text-white', 'shadow-lg');
      btnEl.classList.remove('bg-slate-900/90', 'border-slate-800', 'text-slate-300');

      // Update header badges
      document.getElementById('pillText').innerText = pillText;
      document.getElementById('resolutionTag').innerText = resolution.replace('x', ' × ') + (ratio === '9:16' ? ' (FHD)' : ' (HD)');

      // Dynamically morph viewport container frame
      const frame = document.getElementById('viewportContainer');
      const notch = document.getElementById('notchHeader');
      const frameIcon = document.getElementById('frameIcon');

      // Reset classes
      frame.classList.remove('phone-mockup-frame', 'monitor-mockup-frame', 'aspect-9-16', 'aspect-1-1', 'aspect-16-9', 'max-w-[290px]', 'max-w-[340px]', 'max-w-[520px]', 'rounded-[42px]', 'rounded-3xl', 'rounded-2xl');

      if (ratio === '9:16') {
        frame.classList.add('phone-mockup-frame', 'aspect-9-16', 'max-w-[290px]', 'rounded-[42px]');
        notch.classList.remove('hidden');
        frameIcon.innerText = '📱';
        document.getElementById('frameTitle').innerText = 'iPhone 16 Pro Viewport';
      } else if (ratio === '1:1') {
        frame.classList.add('phone-mockup-frame', 'aspect-1-1', 'max-w-[340px]', 'rounded-3xl');
        notch.classList.add('hidden');
        frameIcon.innerText = '🟦';
        document.getElementById('frameTitle').innerText = 'Square Feed Viewport (1:1)';
      } else {
        frame.classList.add('monitor-mockup-frame', 'aspect-16-9', 'max-w-[520px]', 'rounded-2xl');
        notch.classList.add('hidden');
        frameIcon.innerText = '🖥';
        document.getElementById('frameTitle').innerText = 'Desktop 16:9 Viewport';
      }
    }

    // Set duration presets
    function setDurationTarget(minSec, maxSec, btnEl) {
      minDuration = minSec;
      maxDuration = maxSec;
      document.querySelectorAll('.dur-btn').forEach(btn => {
        btn.classList.remove('bg-brand-950/40', 'border-brand-500', 'text-white', 'shadow-sm');
        btn.classList.add('bg-slate-900/90', 'border-slate-800', 'text-slate-300');
      });
      btnEl.classList.add('bg-brand-950/40', 'border-brand-500', 'text-white', 'shadow-sm');
      btnEl.classList.remove('bg-slate-900/90', 'border-slate-800', 'text-slate-300');
    }

    // Clipboard helper
    async function pasteClipboard() {
      try {
        const text = await navigator.clipboard.readText();
        if (text) document.getElementById('youtubeUrl').value = text;
      } catch (e) {
        // Fallback or permission block
      }
    }

    // Submit extraction job to backend
    async function startGeneration() {
      const youtubeUrl = document.getElementById('youtubeUrl').value.trim();
      const customName = document.getElementById('customName').value.trim() || "Emvic_Clip";
      const groqKey = document.getElementById('groqKey').value.trim();
      const numClips = parseInt(document.getElementById('numClips').value);

      if (!youtubeUrl) {
        showError("Please enter a valid YouTube video link.");
        return;
      }

      // UI state update
      document.getElementById('generateBtn').disabled = true;
      document.getElementById('generateBtn').classList.add('opacity-50', 'cursor-not-allowed');
      document.getElementById('statusContainer').classList.remove('hidden');
      document.getElementById('errorAlert').classList.add('hidden');
      document.getElementById('spinner').classList.remove('hidden');
      document.getElementById('stageLabel').innerText = "Queuing Task";
      document.getElementById('statusStep').innerText = "Initiating extraction pipeline with " + currentAspectRatio + " framing...";
      updateSteps(1);

      try {
        const payload = {
          youtube_url: youtubeUrl,
          custom_name: customName,
          groq_key: groqKey,
          num_clips: numClips,
          aspect_ratio: currentAspectRatio,
          min_duration: minDuration,
          max_duration: maxDuration
        };

        const res = await fetch('/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.message || "Failed to trigger processing job.");
        }

        pollInterval = setInterval(pollStatus, 2000);
      } catch (err) {
        showError(err.message);
      }
    }

    // Poll status from FastAPI
    async function pollStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();

        if (data.status === "processing") {
          document.getElementById('stageLabel').innerText = "Processing Stage";
          document.getElementById('statusStep').innerText = data.step;

          if (data.step.includes("Downloading audio")) {
            updateSteps(1);
          } else if (data.step.includes("analyzing") || data.step.includes("Transcribing")) {
            updateSteps(2);
          } else if (data.step.includes("Rendering")) {
            updateSteps(3);
          }
        } else if (data.status === "completed") {
          clearInterval(pollInterval);
          document.getElementById('stageLabel').innerText = "Generation Complete";
          document.getElementById('statusStep').innerText = "All " + data.clips.length + " clips generated with " + currentAspectRatio + " framing!";
          document.getElementById('spinner').classList.add('hidden');
          updateSteps(3);
          renderClips(data.clips);
          resetButton();
        } else if (data.status === "error") {
          clearInterval(pollInterval);
          showError(data.error || "An error occurred during pipeline execution.");
        }
      } catch (err) {
        console.error("Polling error:", err);
      }
    }

    function updateSteps(stepNum) {
      const d1 = document.getElementById('stepDot1');
      const d2 = document.getElementById('stepDot2');
      const d3 = document.getElementById('stepDot3');

      d1.className = "h-1.5 rounded-full " + (stepNum >= 1 ? "bg-brand-500 shadow-sm shadow-brand-500" : "bg-slate-800");
      d2.className = "h-1.5 rounded-full " + (stepNum >= 2 ? "bg-brand-500 shadow-sm shadow-brand-500" : "bg-slate-800");
      d3.className = "h-1.5 rounded-full " + (stepNum >= 3 ? "bg-emerald-400 shadow-sm shadow-emerald-400" : "bg-slate-800");
    }

    function renderClips(clips) {
      if (!clips || clips.length === 0) return;

      document.getElementById('exportedCountTag').innerText = clips.length + " Clips Exported";
      const gallerySection = document.getElementById('gallerySection');
      const clipsGrid = document.getElementById('clipsGrid');
      clipsGrid.innerHTML = '';
      gallerySection.classList.remove('hidden');

      // Load 1st clip into primary preview viewport
      playClipInPreview(clips[0]);

      clips.forEach((clip, idx) => {
        const card = document.createElement('div');
        card.className = "glass-panel rounded-2xl p-4 flex flex-col justify-between border border-slate-800 hover:border-slate-700 transition space-y-3 shadow-xl";
        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between text-xs mb-2">
              <span class="font-bold text-white font-mono">#${idx + 1} Clip</span>
              <span class="text-[10px] bg-slate-900 border border-slate-800 text-brand-400 px-2 py-0.5 rounded font-mono font-bold">${clip.duration}s</span>
            </div>
            <h4 class="text-xs font-semibold text-slate-200 line-clamp-2 leading-relaxed">${clip.title}</h4>
          </div>
          
          <div class="flex items-center gap-2 pt-2 border-t border-slate-800/80">
            <button type="button" onclick='playClipInPreview(${JSON.stringify(clip)})' class="flex-1 bg-slate-900 hover:bg-slate-800 active:scale-[0.98] text-slate-200 text-xs font-bold py-2 rounded-xl border border-slate-700 transition flex items-center justify-center gap-1.5">
              <span>▶</span>
              <span>Preview</span>
            </button>
            <a href="${clip.url}" download="${clip.filename}" class="flex-1 bg-brand-600 hover:bg-brand-500 active:scale-[0.98] text-white text-xs font-bold py-2 rounded-xl transition flex items-center justify-center gap-1.5 shadow-md shadow-brand-600/20">
              <span>⬇</span>
              <span>Download</span>
            </a>
          </div>
        `;
        clipsGrid.appendChild(card);
      });
    }

    function playClipInPreview(clip) {
      currentClipUrl = window.location.origin + clip.url;
      const player = document.getElementById('previewPlayer');
      const placeholder = document.getElementById('previewPlaceholder');
      const activeBar = document.getElementById('activeClipBar');
      const previewActions = document.getElementById('previewActions');

      placeholder.classList.add('hidden');
      player.classList.remove('hidden');
      activeBar.classList.remove('hidden');
      previewActions.classList.remove('hidden');

      document.getElementById('activeClipTitle').innerText = clip.title;
      document.getElementById('activeClipAspectBadge').innerText = currentAspectRatio + " FHD";
      document.getElementById('downloadActiveBtn').href = clip.url;
      document.getElementById('downloadActiveBtn').download = clip.filename;

      player.src = clip.url;
      player.load();
      player.play().catch(() => {});
    }

    function copyCurrentClipLink() {
      if (!currentClipUrl) return;
      const dummy = document.createElement("input");
      document.body.appendChild(dummy);
      dummy.value = currentClipUrl;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);

      const copyLabel = document.getElementById('copyLinkText');
      copyLabel.innerText = "Link Copied!";
      setTimeout(() => { copyLabel.innerText = "Copy Video Link"; }, 2000);
    }

    function showError(msg) {
      document.getElementById('spinner').classList.add('hidden');
      document.getElementById('stageLabel').innerText = "Task Error";
      document.getElementById('statusStep').innerText = "Process encountered an error.";
      const errBox = document.getElementById('errorAlert');
      errBox.innerText = msg;
      errBox.classList.remove('hidden');
      resetButton();
    }

    function resetButton() {
      document.getElementById('generateBtn').disabled = false;
      document.getElementById('generateBtn').classList.remove('opacity-50', 'cursor-not-allowed');
    }
  </script>
</body>
</html>
