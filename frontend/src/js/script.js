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

function putVariant(data) {
  return putToBackend('/variant', data);
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
    console.log(response);
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
    console.log(response);

    // Update der Ausgabehistorie
    updateOutputHistory(response);

    // Entfernen der Hervorhebung nach einer kurzen Verzögerung
    setTimeout(() => {
      findAndHighlightKey(keyboard_input, keyText, false);
    }, 2000);
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

