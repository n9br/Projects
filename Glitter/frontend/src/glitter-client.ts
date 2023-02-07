console.log("Hallo from an-glitter-client.js");

/**
 * ✅ 1. Daten holen   JSON von NodeJS (auspacken ?)
 * ✅ 1.5 Klasse Glit definieren zur Verwendung
 * ✅ 2. Daten aufbereiten
 * ✅ 3. Card erzeugen
 * ✅ 4. Card anzeigen
 */

/**
 * id: userID
 * user: string
 * text: string
 * datetime: datetime / string 
 */

class Glit {
    // id: number;
    avatarId: number;
    user: string;
    text: string;
    datetime: string;

    constructor(data: { avatarId: number; user: string; text: string; datetime: string | number | Date; }) {
        // this.id = data.id;
        this.avatarId = data.avatarId;
        this.user = data.user;
        this.text = data.text;
        this.datetime = new Date(data.datetime).toLocaleDateString() + " " + new Date(data.datetime).toLocaleTimeString();
    }
}

function getRandomInt(max: number) {
	return Math.floor(Math.random() * (max + 1));
}

// const dateFormat = require('dateformat');
function renderCard(glit: Glit) {

        // <div class="uk-child-width-1-2@s" uk-grid>
    //     <div>
    //         <div class="uk-card uk-card-default uk-card-small uk-card-body">
    //             <h3 class="uk-card-title">${glit.title}</h3>
    //             <p>${glit.text}</p>
    //         </div>
    //     </div>
    // </div>

    return `  
    <div class="uk-card uk-card-default uk-width-1-2@m gl-container-center" style="margin-bottom: 30px;">
        <div class="uk-card-header">
            <div class="uk-grid-small uk-flex-middle" uk-grid>
                <div class="uk-width-auto">
                    <img class="uk-border-circle" width="40" height="40" src="https://i.pravatar.cc/${glit.avatarId}" alt="Avatar">
                </div>
                <div class="uk-width-expand">
                    <h3 class="uk-card-title uk-margin-remove-bottom">${glit.user}</h3>
                    <p class="uk-text-meta uk-margin-remove-top"><time>${glit.datetime}</time></p>
                </div>
            </div>
        </div>
        <div class="uk-card-body">
            <p>${glit.text}</p>
        </div>
    </div>
    `
}

function getGlitsFromBackend() {
    fetch("http://localhost:4000/glits")
        // .then(res => console.log(res))
        .then(res => res.json())
        // .then(json => console.log(json))
        .then(json => appendData(json))
        // .then(json => console.log(json.map(json)))

        // Djordje's Version
        // .then(json => {
        //     const glitts = json.map(glitt => new Glitt(glitt))
        //     displayGlitts(glitts)
        
        function appendData(data) {
            let glit: Glit;
            let glitRender: string;
            for (var i = 0; i < data.length; i++) {
                glit = new Glit(data[i]);     // write to JS object
                console.log("Hello from appendData - handling: ");
                console.log(glit);
                glitRender = renderCard(glit);
                document.getElementById("gl-card-container")!.innerHTML += glitRender; 
            }        
        }
}

function saveGlit() {
    const glitUser = (<HTMLInputElement>document.getElementById("gl-glituser")).value;
    const glitText = (<HTMLTextAreaElement>document.getElementById("gl-glittext")).value;
    const avatarId = getRandomInt(150);
    postGlitToBackend(glitUser, glitText, avatarId);
}

function postGlitToBackend(glitUser: string, glitText: string, avatarId: number) {

    fetch('http://localhost:4000/glits', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
                user: glitUser,
                avatarId: avatarId,
                text: glitText,
                datetime: new Date()
        })
    })
    .then(res => console.log(res))
    // .then(res => res.json())
    // .then(res => console.log(JSON.stringify(res)))
    // .then(res => {
    //     if (res.status === 201) {
    //         UIkit.notification({
    //             message: "Glitt created!",
    //             status: "success",
    //             pos: "bottom-center",
    //             timeout: 3_000
    //         });
    //         resetForm()
    //         getGlittsFromBackend()
    //         hideModal()
    //     }
    // })
}

// Main
getGlitsFromBackend()