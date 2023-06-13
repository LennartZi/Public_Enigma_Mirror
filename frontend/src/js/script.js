const variantSelect = document.getElementById('variantSelect');
const inputHistory = document.getElementById('inputHistory');
const outputHistory = document.getElementById('outputHistory');
const keyboard_input = document.getElementById('keyboard_input');
const keyboard_output = document.getElementById('keyboard_output');
const keyboard_plug = document.getElementById('keyboard_plug');

const maxHistoryLength = 140;
const backendUrl = location.origin + '/api';
const connections = {};
let selectedKeys = [];

const rows = [
  'qwertyuiop',
  'asdfghjkl',
  'zxcvbnm'
];

const plug_row = [
  'qwertyuio',
  'asdfghjk',
  'pzxcvbnml'
];

// Senden und Empfangen von Daten vom Backend
async function putToBackend(directory, data) {
  try {
    const response = await fetch(backendUrl + directory, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),

    });
    return await response.json();
  } catch (error) {
    console.error('Fehler beim Senden der Daten ans Backend:', error);
    throw error;
  }
}

async function getFromBackend(directory) {
  try {
    const response = await fetch(backendUrl + directory, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return await response.json();
  } catch (error) {
    console.error('Fehler beim Senden der Daten ans Backend:', error);
    throw error;
  }
}

//API Calls
function getHistory() {
  return getFromBackend('/history');
}
function putKey(data) {
  return putToBackend('/encrypt', data);
}

function getVariants() {
  return getFromBackend('/variants');
}
function getVariant() {
  return getFromBackend('/variant');
}

function putVariant(data) {
  return putToBackend('/variant', data);
}
function getRotors() {
  return getFromBackend('/rotors');
}

function getRotor(position) {
    return getFromBackend(`/rotor/${position}`);
}

function putRotors(position, data) {
    return putToBackend(`/rotor/${position}`, data);
}

<<<<<<< frontend/src/js/script.js
function getReflectors() {
    return getFromBackend(`/reflectors`);
}

function putReflectors(data) {
    return putToBackend(`/reflector`, data);
}

function getReflector() {
    return getFromBackend(`/reflector`);
}
function putPlug(data) {
    return putToBackend(`/plugboard`, data);
}

function getPlug() {
    return getFromBackend(`/plugboard`);
}

// Erstellen der Tasten
function createKeys(keyboardDiv) {
  for (let rowIndex = 0; rowIndex < rows.length; rowIndex++) {
    const row = document.createElement('div');
    row.classList.add('row');
    const keys = rows[rowIndex];

    for (let i = 0; i < keys.length; i++) {
      const key = document.createElement('div');
      key.classList.add('key_input');
      key.textContent = keys[i].toUpperCase();
      // Füge den Mausklick-Event-Listener hinzu, wenn das Tasten-Element erstellt wird
      if (keyboardDiv === keyboard_input) {
        addClickListener(key);
      }
      row.appendChild(key);
    }

    keyboardDiv.appendChild(row);
  }
}

createKeys(keyboard_input);


function createOutput(keyboardDiv) {
  for (let rowIndex = 0; rowIndex < plug_row.length; rowIndex++) {
    const row = document.createElement('div');
    row.classList.add('row');
    const keys = plug_row[rowIndex];

    for (let i = 0; i < keys.length; i++) {
      const key = document.createElement('div');
      key.classList.add('key_output');
      key.textContent = keys[i].toUpperCase();
      row.appendChild(key);
    }
    keyboardDiv.appendChild(row);
  }
  //addKeyListeners(keyboardDiv);
}

createOutput(keyboard_output);


// Event-Listener zum Abfangen von Tastenanschlägen
document.addEventListener('keydown', async (event) => {
  if (isVariantSelected()) return;
  const key = event.key;

  // Prüfe, ob der gedrückte Buchstabe in den `rows` enthalten ist
  const isValidKey = rows.some(row => row.includes(key.toLowerCase()));

  if (!event.repeat && isValidKey) {
    updateInputHistory(key);
    findAndHighlightKey(keyboard_input, key , true);
    const response = await putKey({letter: key})
    findAndHighlightKey(keyboard_output, response, true);
    // Output History aktualisieren
    updateOutputHistory(response);
  }
});

document.addEventListener('keyup', async (event) => {
  if (isVariantSelected()) return;
  const key = event.key;

  findAndHighlightKey(keyboard_input, key , false);
  findAndHighlightKey(keyboard_output, outputHistory.textContent[0], false);

});



// Hilfsfunktion, um die Tasten zu finden und hervorzuheben
function findAndHighlightKey(keyboardDiv, key, highlight) {
  const isKeyInput = keyboardDiv === keyboard_input;
  const keys = keyboardDiv.getElementsByClassName(isKeyInput ? 'key_input' : 'key_output');
  const highlightClass = keyboardDiv === keyboard_input ? 'highlight' : 'highlight-red';
  for (let k of keys) {
    if (k.textContent.toLowerCase() === key.toLowerCase()) {
      if (highlight) {
        k.classList.add(highlightClass);
      } else {
        k.classList.remove(highlightClass);
      }
      break;
    }
  }
}

// Funktion zum Hinzufügen des Mausklick-Event-Listeners
function addClickListener(key) {
  key.addEventListener('click', async () => {
    if (isVariantSelected()) return;
    const keyText = key.textContent;
    updateInputHistory(keyText);
    findAndHighlightKey(keyboard_input, keyText, true);
    const response = await putKey({ letter: keyText });
    findAndHighlightKey(keyboard_output, response, true);

    // Update der Ausgabehistorie
    updateOutputHistory(response);

    // Entfernen der Hervorhebung nach einer kurzen Verzögerung
    setTimeout(() => {
      findAndHighlightKey(keyboard_input, keyText, false);
      findAndHighlightKey(keyboard_output, response, false);
    }, 1000);
  });
}


// Funktion zum Aktualisieren der Eingabehistorie
function updateInputHistory(clickedKey) {
  inputHistory.textContent = (clickedKey.toUpperCase() + inputHistory.textContent).substring(0, maxHistoryLength);
}

// Funktion zum Aktualisieren der Ausgabehistorie
function updateOutputHistory(output) {
  outputHistory.textContent = (output.toUpperCase() + outputHistory.textContent).substring(0, maxHistoryLength);
}


function loadHistory() {
  getHistory().then(history => {
    outputHistory.textContent = history.history.split('').reverse().join('').toUpperCase();
    inputHistory.textContent = history.input_history.split('').reverse().join('').toUpperCase();
  });
}


async function VariantsDropdown() {
  try {
    const variants = await getVariants();
    for (let variant of variants) {
      const option = document.createElement('option');
      option.value = variant;
      option.text = variant;
      variantSelect.appendChild(option);
    }
  } catch (error) {
    console.error('Error while populating variant dropdown:', error);
  }
}

async function updateRotorOptions() {
  try {
    const rotors = await getRotors();
    const rotorCount = rotors.length;

    const rotorSelection = document.getElementById('rotorSelection');
    rotorSelection.innerHTML = '';

    for (let i = 0; i < rotorCount; i++) {
      const li = document.createElement("li");
      li.textContent = rotors[i].name;
      li.setAttribute("data-value", "rotor" + (i + 1));

      li.addEventListener("click", async function(event) {
        const selectedItems = rotorSelection.querySelectorAll("li.selected");
        const selectedRotorList = document.getElementById('selectedRotor');

        if (event.target.classList.contains("selected")) {
          event.target.classList.remove("selected");

          for (let item of selectedRotorList.children) {
            if (item.textContent === event.target.textContent) {
              item.textContent = 'X';
              break;
            }
          }
          return;
        }

        if (selectedItems.length < 3) {
          event.target.classList.add("selected");

          // Find the index of the first 'X' item
          let rotorPosition;
          for (let i = 0; i < selectedRotorList.children.length; i++) {
            if (selectedRotorList.children[i].textContent === 'X') {
              selectedRotorList.children[i].textContent = event.target.textContent;
              rotorPosition = i;
              break;
            }
          }

          try {
            const rotorName = event.target.textContent;
            await putRotors(rotorPosition, { rotor: rotorName });
          } catch (error) {
            console.error('Error while sending the selected rotor to the backend:', error);
          }
        }
      });
      rotorSelection.appendChild(li);
    }
  } catch (error) {
    console.error('Error while updating rotor options:', error);
  }
}


window.addEventListener('load', async(event) => {
  await VariantsDropdown();
  const variant = await getVariant();
  if (variant !== undefined) {
    document.getElementById('variantSelect').value = variant;
  }
  await updateRotorOptions();
  await updateRotors();
  await updateReflectorOptions();
  await updateReflectors();
  loadPlug();
  loadHistory();
});

document.getElementById('variantSelect').addEventListener('change', async(event) => {
  const enigmaModel = document.getElementById('variantSelect');
  await putVariant({variant: enigmaModel.value});
  await updateRotorOptions();
  await updateReflectorOptions();
  document.cookie = 'rotors=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  document.cookie = 'reflector=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
});


variantSelect.addEventListener('change', function() {
  const selectedRotorList = document.getElementById('selectedRotor');
  const rotorSelection = document.getElementById('rotorSelection');

  // Set the content of all li elements in the selectedRotorList to 'X'
  for (let item of selectedRotorList.children) {
    item.textContent = 'X';
  }

  // Deselect all selected items in the rotorSelection list
  const selectedItems = rotorSelection.querySelectorAll("li.selected");
  for (let item of selectedItems) {
    item.classList.remove('selected');
  }
});



async function updateRotors() {
    const selectedRotorList = document.getElementById('selectedRotor');
    const rotorSelection = document.getElementById('rotorSelection');

    for (let i = 0; i < 3; i++) {
        try {
            const response = await getRotor(i);
            if (response && response.rotor) {
                selectedRotorList.children[i].textContent = response.rotor;

                // Finden und Auswählen des entsprechenden Rotors in der rotorSelection
                for (let rotorOption of rotorSelection.children) {
                    if (rotorOption.textContent === response.rotor) {
                        rotorOption.classList.add('selected');
                        break;
                    }
                }
            }
        } catch (error) {
            // Ignoriere Fehler mit dem Statuscode 400 und lasse den textContent unverändert
            if (error.status !== 400) {
                console.error(`Fehler beim Abrufen des Rotors an der Position ${i}:`, error);
            }
        }
    }
}

function isVariantSelected() {
  const rotorSelection = document.getElementById('rotorSelection');
  const selectedRotors = rotorSelection.querySelectorAll("li.selected");


  // Wenn kein Variante ausgewählt ist oder keine Rotoren ausgewählt sind, gebe true zurück
  if (variantSelect.value === '' || selectedRotors.length < 3 || variantSelect.value === 'B' && selectedRotors.length < 2) {
    return true;
  }
}

async function updateReflectorOptions() {
  try {
    const reflectors = await getReflectors();
    const reflectorCount = reflectors.length;

    const reflectorSelection = document.getElementById('reflectorSelection');
    reflectorSelection.innerHTML = '';

    for (let i = 0; i < reflectorCount; i++) {
      const li = document.createElement("li");
      li.textContent = reflectors[i].name;
      li.setAttribute("data-value", "reflector" + (i + 1));

      li.addEventListener("click", async function(event) {
        const selectedItems = reflectorSelection.querySelectorAll("li.selected");

        if (event.target.classList.contains("selected")) {
          event.target.classList.remove("selected");
          return;
        }

        if (selectedItems.length < 1) { // Adjust this condition based on your requirements
          event.target.classList.add("selected");
          try {
            const reflectorName = event.target.textContent;
            await putReflectors({ reflector: reflectorName });
          } catch (error) {
            console.error('Error while sending the selected reflector to the backend:', error);
          }
        }
      });
      reflectorSelection.appendChild(li);
    }
  } catch (error) {
    console.error('Error while updating reflector options:', error);
  }
}

async function updateReflectors() {
  const reflectorSelection = document.getElementById('reflectorSelection');

  try {
    const response = await getReflector();
    if (response && response.reflector) {
      // Finden und Auswählen des entsprechenden Reflektors in der reflectorSelection
      for (let reflectorOption of reflectorSelection.children) {
        if (reflectorOption.textContent === response.reflector) {
          reflectorOption.classList.add('selected');
          break;
        }
      }
    }
  } catch (error) {
    // Ignoriere Fehler mit dem Statuscode 400 und lasse den textContent unverändert
    if (error.status !== 400) {
      console.error(`Fehler beim Abrufen des Reflectors:`, error);
    }
  }
}

function createPlug(keyboardDiv, keysConfig) {
  for (let rowIndex = 0; rowIndex < keysConfig.length; rowIndex++) {
    const row = document.createElement('div');
    row.classList.add('row');
    const keys = keysConfig[rowIndex];

    for (let i = 0; i < keys.length; i++) {
      const key = document.createElement('div');
      key.classList.add('key_plug');
      key.textContent = keys[i].toUpperCase();
      key.addEventListener('click', () => {
          handlePlugClick(key);});
      row.appendChild(key);
    }
    keyboardDiv.appendChild(row);
  }
}

createPlug(keyboard_plug, plug_row);


function handlePlugClick(key) {
  // Wenn die Taste bereits verbunden ist, trenne sie
  if (connections[key.textContent]) {
    disconnectKeys(key);
    return;
  }

  // Wenn die maximale Anzahl von Verbindungen erreicht ist, kehre frühzeitig zurück
  if (Object.keys(connections).length >= 10) {
    return;
  }

  // Wechsle die 'selected'-Klasse für die geklickte Taste und aktualisiere das ausgewählte Tastenarray
  toggleSelectedClass(key);
  updateSelectedKeys(key);

  // Verbinde die Tasten, wenn zwei Tasten ausgewählt sind
  if (selectedKeys.length === 2) {
    const [key1, key2] = selectedKeys;
    const color = getRandomColor();
    key1.style.backgroundColor = color;
    key2.style.backgroundColor = color;
    connectKeys(key1, key2);
  }
}

function loadPlug() {
  getPlug().then(response => {
    if (response) {
      const uniqueEntries = [];
      for (const [key, value] of Object.entries(response)) {
        // Überprüfen, ob das Paar bereits im Array vorhanden ist, aber in umgekehrter Reihenfolge
        if (!uniqueEntries.find(([k, v]) => k === value && v === key)) {
          uniqueEntries.push([key, value]);
        }
      }

      for (const [key, value] of uniqueEntries) {
        const color = getRandomColor();

        const keyElements = Array.from(document.querySelectorAll('.key_plug'));
        const keyElement = keyElements.find(element => element.textContent === key);
        const valueElement = keyElements.find(element => element.textContent === value);

        if (keyElement && valueElement) {
          toggleSelectedClass(keyElement);
          toggleSelectedClass(valueElement);
          keyElement.style.backgroundColor = color;
          valueElement.style.backgroundColor = color;
          connectKeys(keyElement, valueElement);
        }
      }
    }
  });
}

function disconnectKeys(key) {
  const connectedKey = connections[key.textContent].key;
  delete connections[key.textContent];
  delete connections[connectedKey.textContent];
  key.style.backgroundColor = "";
  connectedKey.style.backgroundColor = "";
  toggleSelectedClass(key);
  toggleSelectedClass(connectedKey);

  // Update the connections object format after disconnecting keys
  const connectionEntries = Object.entries(connections);
  const connectionTextContentPairs = connectionEntries.map(([k, v]) => [k, v.key.textContent]);
  const connectionObject = Object.fromEntries(connectionTextContentPairs);

  // Wrap the connectionObject in a "plugboard" object
  const finalObject = { plugboard: connectionObject };

  putPlug(finalObject).then(r => console.log(r));
}

function connectKeys(key1, key2) {
  connections[key1.textContent] = { key: key2};
  connections[key2.textContent] = { key: key1};
  selectedKeys = [];

  const connectionEntries = Object.entries(connections);
  const connectionTextContentPairs = connectionEntries.map(([k, v]) => [k, v.key.textContent]);
  const connectionObject = Object.fromEntries(connectionTextContentPairs);
  const finalObject = { plugboard: connectionObject };
  putPlug(finalObject).then(r => console.log(r));
}

function toggleSelectedClass(key) {
  console.log(`Toggling selected class for key: ${key.textContent}`);
  key.classList.toggle('selected');
  console.log(`Key classes after toggle: ${key.classList}`);
}

function updateSelectedKeys(key) {
  if (selectedKeys.includes(key)) {
    selectedKeys = selectedKeys.filter(k => k !== key);
  } else {
    selectedKeys.push(key);
  }
}

const availableColors = [
  '#FF0000', // Rot
  '#00FF00', // Grün
  '#0000FF', // Blau
  '#FFFF00', // Gelb
  '#FF00FF', // Magenta
];

function getRandomColor() {
  if (availableColors.length === 0) {
    throw new Error('Es sind keine Farben mehr verfügbar.');
  }

  const randomIndex = Math.floor(Math.random() * availableColors.length);
  const color = availableColors[randomIndex];

  // Entfernen Sie die verwendete Farbe aus dem Array, um Duplikate zu verhindern
  availableColors.splice(randomIndex, 1);

  return color;
}