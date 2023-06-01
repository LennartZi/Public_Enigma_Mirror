const variantSelect = document.getElementById('variantSelect');
const inputHistory = document.getElementById('inputHistory');
const outputHistory = document.getElementById('outputHistory');
const keyboard_input = document.getElementById('keyboard_input');
const maxHistoryLength = 140;
const backendUrl = location.origin + '/api';

const rows = [
  'qwertyuiop',
  'asdfghjkl',
  'zxcvbnm'
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


// Event-Listener zum Abfangen von Tastenanschlägen
document.addEventListener('keydown', async (event) => {
  const key = event.key;

  // Prüfe, ob der gedrückte Buchstabe in den `rows` enthalten ist
  const isValidKey = rows.some(row => row.includes(key.toLowerCase()));

  if (!event.repeat && isValidKey) {
    updateInputHistory(key);
    findAndHighlightKey(keyboard_input, key , true);
    const response = await putKey({letter: key})
    // Output History aktualisieren
    updateOutputHistory(response);
  }
});

document.addEventListener('keyup', async (event) => {
  const key = event.key;

  findAndHighlightKey(keyboard_input, key , false);

});



// Hilfsfunktion, um die Tasten zu finden und hervorzuheben
function findAndHighlightKey(keyboardDiv, key, highlight) {
  const keys = keyboardDiv.getElementsByClassName('key_input');
  const highlightClass = 'highlight';
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
    const keyText = key.textContent;
    updateInputHistory(keyText);
    findAndHighlightKey(keyboard_input, keyText, true);
    const response = await putKey({ letter: keyText });

    // Update der Ausgabehistorie
    updateOutputHistory(response);

    // Entfernen der Hervorhebung nach einer kurzen Verzögerung
    setTimeout(() => {
      findAndHighlightKey(keyboard_input, keyText, false);
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
  loadHistory();
});

document.getElementById('variantSelect').addEventListener('change', async(event) => {
  const enigmaModel = document.getElementById('variantSelect');
  await putVariant({variant: enigmaModel.value});
  await updateRotorOptions();
  document.cookie = 'rotors=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
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