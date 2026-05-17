# AC-Copy-Method

**CREDITS:**

loony2HP - Developer

rain - Copy Helper

**1. Setup Backend**
- Grab the backend and open a txt editor

**2. Install Base APK**
- Use QuestAppVersionSwitcher to get target APK version
- Go to the /gamedata folder in this repo and click one of the updates then copy the url
- Go into the backend and replace the url placeholder with the gamedata url
- Decompile APK

**3. BackendLIB**
- Find a lib src for backend (xera company lib for example)
- Edit it with your backend
- Compile lib
- Inject into AC Copy

**4. Create a Photon**
- Head to photonengine.org
- Create a voice app id then go into backend and replace voice app id placeholder with yours
- Head back to Photon
- Develop a Fusion 2 app id, go to pythonanywhere, copy ur url, add a /auth to the end so com/auth
- Go back to photon and paste in your url as custom auth, create the app
- Copy app id and paste it in app id placeholder in backend

**5. Deploy Edited Backend**
- Deploy, reload pythonanywhere web project

**6. Play your game**
- You are done!
