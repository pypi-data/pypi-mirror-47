

// Model for loading Projects, Screens and their Map Annotations
let model = new StudiesModel();
let mapr_settings;

function renderStudyKeys() {
  let html = FILTER_KEYS
      .map(key => {
        if (key.label && key.value) {
          return `<option value="${ key.value }">${ key.label }</option>`
        }
        return `<option value="${ key }">${ key }</option>`
      })
      .join("\n");
  document.getElementById('studyKeys').innerHTML = html;
}
renderStudyKeys();


// FIRST, populate forms from query string
function populateInputsFromSearch() {
  let search = window.location.search.substr(1);
  let query = '';
  var searchParams = search.split('&');
  for (var i = 0; i < searchParams.length; i++) {
    var paramSplit = searchParams[i].split('=');
    if (paramSplit[0] === 'query') {
        query = paramSplit[1].replace(/%20/g, " ");
    }
  }
  if (query) {
    let splitIndex = query.indexOf(':');
    let configId = query.slice(0, splitIndex);
    let value = query.slice(splitIndex + 1);
    if (configId && value) {
      document.getElementById("maprConfig").value = configId;
      document.getElementById("maprQuery").value = value;
      let key = configId.replace('mapr_', '');
      let placeholder = key;
      if (mapr_settings && mapr_settings[key]) {
        placeholder = mapr_settings[key].all.join(", ");
      }
      document.getElementById('maprQuery').placeholder = placeholder;
    }
  }
}
populateInputsFromSearch();


// ------------ Handle MAPR searching or filtering --------------------- 

function filterStudiesByMapr(value) {
  $('#studies').removeClass('studiesLayout');
  let configId = document.getElementById("maprConfig").value.replace("mapr_", "");
  document.getElementById('studies').innerHTML = "";
  let key = mapr_settings[value] ? mapr_settings[value].all.join(" or ") : value;
  showFilterSpinner(`Finding images with ${ configId }: ${ value }...`);

  // First, get all terms that match (NOT case_sensitive)
  // /mapr/api/gene/?value=TOP2&case_sensitive=false&orphaned=true
  let url = `${ BASE_URL }mapr/api/${ configId }/?value=${ value }&case_sensitive=false&orphaned=true`;
  $.getJSON(url, (data) => {
    renderMaprMessage(data.maps);
    data.maps.forEach(termData => {
      let term = termData.id;

      renderMaprResults(term)
    });
  });
}


function renderMaprMessage(mapsData) {
  let studyCount = mapsData.reduce((count, data) => count + data.childCount, 0);
  let imageCount = mapsData.reduce((count, data) => count + data.extra.counter, 0);
  let terms = mapsData.map(d => d.id).join('/');
  let filterMessage = "";
  if (mapsData.length === 0) {
    filterMessage = noStudiesMessage();
  } else {
    let configId = document.getElementById("maprConfig").value.replace('mapr_', '');
    let key = configId;
    if (mapr_settings && mapr_settings[configId]) {
      key = mapr_settings[key].label;
    }
    filterMessage = `<p class="filterMessage">
      Found <strong>${ imageCount }</strong> images with
      <strong>${key}</strong>: <strong>${terms}</strong>
      in <strong>${ studyCount }</strong> stud${ studyCount == 1 ? 'y' : 'ies' }</strong></p>`;
  }
  document.getElementById('filterCount').innerHTML = filterMessage;
}


function renderMaprResults(term) {
  let configId = document.getElementById("maprConfig").value.replace("mapr_", "");

  let elementId = 'maprResultsTable' + term;
  let html = `
    <h2>${ term }</h2>
    <table class='maprResultsTable' style='margin-top:20px'>
      <tbody data-id='${ elementId }'>
        <tr>
          <th>Study ID</th>
          <th>Organism</th>
          <th>Image count</th>
          <th>Title</th>
          <th>Sample Images</th>
          <th>Link</th>
        </tr>
      </tbody>
    </table>`;
  $('#studies').append(html);


  let url = `${ BASE_URL }mapr/api/${ configId }/?value=${ term }`;
  $.getJSON(url, (data) => {
    // filter studies by 'screens' and 'projects'
    let imageCounts = {};
    data.screens.forEach(s => {imageCounts[`screen-${ s.id }`] = s.extra.counter});
    data.projects.forEach(s => {imageCounts[`project-${ s.id }`] = s.extra.counter});

    let filterFunc = study => {
      let studyId = study['@type'].split('#')[1].toLowerCase() + '-' + study['@id'];
      return imageCounts.hasOwnProperty(studyId);
    }

    let maprData = model.studies.filter(filterFunc).map(study => {
      let studyId = study['@type'].split('#')[1].toLowerCase() + '-' + study['@id'];
      let studyData = Object.assign({}, study);
      studyData.imageCount = imageCounts[studyId];
      return studyData;
    });
    renderMapr(maprData, term);
  })
  .fail(() => {
    document.getElementById('filterCount').innerHTML = "Request failed. Server may be busy."
  })
  .always(() => {
    hideFilterSpinner();
  });
}

// ----- event handling --------

document.getElementById('maprConfig').onchange = (event) => {
  document.getElementById('maprQuery').value = '';
  let value = event.target.value.replace('mapr_', '');
  let placeholder = mapr_settings[value] ? mapr_settings[value].all.join(", ") : value;
  document.getElementById('maprQuery').placeholder = placeholder;
  // Show all autocomplete options...
  $("#maprQuery").focus();
  render();
}

// We want to show auto-complete options when user
// clicks on the field.
function showAutocomplete(event) {
  let configId = document.getElementById("maprConfig").value;
  let autoCompleteValue = event.target.value;
  if (configId.indexOf('mapr_') != 0) {
    // If not MAPR search, show all auto-complete results
    autoCompleteValue = '';
  }
  $("#maprQuery").autocomplete("search", autoCompleteValue);
}

document.getElementById('maprQuery').onfocus = (event) => {
  showAutocomplete(event);
}
document.getElementById('maprQuery').onclick = (event) => {
  // select all the text (easier to type new search term)
  event.target.setSelectionRange(0, event.target.value.length);
  showAutocomplete(event);
}

// ------ AUTO-COMPLETE -------------------

function showSpinner() {
  document.getElementById('spinner').style.visibility = 'visible';
}
function hideSpinner() {
  document.getElementById('spinner').style.visibility = 'hidden';
}
// timeout to avoid flash of spinner
let filterSpinnerTimout;
function showFilterSpinner(message) {
  filterSpinnerTimout = setTimeout(() => {
    document.getElementById('filterSpinnerMessage').innerHTML = message ? message : '';
    document.getElementById('filterSpinner').style.display = 'block';
  }, 500);
}
function hideFilterSpinner() {
  clearTimeout(filterSpinnerTimout);
  document.getElementById('filterSpinnerMessage').innerHTML = '';
  document.getElementById('filterSpinner').style.display = 'none';
}

$("#maprQuery")
    .keyup(event => {
      if (event.which == 13) {
        $(event.target).autocomplete( "close" );
        filterAndRender();
        // Add to browser history. Handled by onpopstate on browser Back
        let configId = document.getElementById("maprConfig").value;
        window.history.pushState({}, "", `?query=${ configId }:${ event.target.value }`);
      }
    })
    .autocomplete({
    autoFocus: false,
    delay: 1000,
    source: function( request, response ) {

        // if configId is not from mapr, we filter on mapValues...
        let configId = document.getElementById("maprConfig").value;
        if (configId.indexOf('mapr_') != 0) {

          let matches;
          if (configId === 'Name') {
            matches = model.getStudiesNames(request.term);
          } else {
            matches = model.getKeyValueAutoComplete(configId, request.term);
          }
          response(matches);

          if (request.term.length === 0) {
            render();
            return;
          }

          filterAndRender();
          return;
        }

        // Don't handle empty query for mapr
        if (request.term.length == 0) {
          return;
        }

        // Auto-complete to filter by mapr...
        configId = configId.replace('mapr_', '');
        let case_sensitive = false;

        let requestData = {
            case_sensitive: case_sensitive,
        }
        let url;
        if (request.term.length === 0) {
          // Try to list all top-level values.
          // This works for 'wild-card' configs where number of values is small e.g. Organism
          // But will return empty list for e.g. Gene
          url = `${ BASE_URL }mapr/api/${ configId }/`;
          requestData.orphaned = true
        } else {
          // Find auto-complete matches
          url = `${ BASE_URL }mapr/api/autocomplete/${ configId }/`;
          requestData.value = case_sensitive ? request.term : request.term.toLowerCase();
          requestData.query = true;   // use a 'like' HQL query
        }

        showSpinner();
        $.ajax({
            dataType: "json",
            type : 'GET',
            url: url,
            data: requestData,
            success: function(data) {
                hideSpinner();
                if (request.term.length === 0) {
                  // Top-level terms in 'maps'
                  if (data.maps && data.maps.length > 0) {
                    let terms = data.maps.map(m => m.id);
                    terms.sort();
                    response(terms);
                  }
                }
                else if (data.length > 0) {
                    response( $.map( data, function(item) {
                        return item;
                    }));
                } else {
                   response([{ label: 'No results found.', value: -1 }]);
                }
            },
            error: function(data) {
                hideSpinner();
                // E.g. status 504 for timeout
                response([{ label: 'Loading auto-complete terms failed. Server may be busy.', value: -1 }]);
            }
        });
    },
    minLength: 0,
    open: function() {},
    close: function() {
        // $(this).val('');
        return false;
    },
    focus: function(event,ui) {},
    select: function(event, ui) {
        if (ui.item.value == -1) {
          // Ignore 'No results found'
          return false;
        }
        $(this).val(ui.item.value);
        filterAndRender();
        // Add to browser history. Handled by onpopstate on browser Back
        let configId = document.getElementById("maprConfig").value;
        window.history.pushState({}, "", `?query=${ configId }:${ ui.item.value }`);

        return false;
    }
}).data("ui-autocomplete")._renderItem = function( ul, item ) {
    return $( "<li>" )
        .append( "<a>" + item.label + "</a>" )
        .appendTo( ul );
}


// ------------ Render -------------------------

function filterAndRender() {
  let configId = document.getElementById("maprConfig").value;
  let value = document.getElementById("maprQuery").value;
  if (!value) {
    render();
    return;
  }
  if (configId.indexOf('mapr_') != 0) {
    // filter studies by Key-Value pairs
    let filterFunc = study => {
      let toMatch = value.toLowerCase();
      if (configId === 'Name') {
        return study.Name.toLowerCase().indexOf(toMatch) > -1;
      }
      // Filter by Map-Annotation Key-Value
      let show = false;
      if (study.mapValues) {
        study.mapValues.forEach(kv => {
          if (kv[0] === configId && kv[1].toLowerCase().indexOf(toMatch) > -1) {
            show = true;
          }
        });
      }
      return show;
    }
    render(filterFunc);
  } else {
    filterStudiesByMapr(value);
  }
}

function renderMapr(maprData, term) {

  maprData.sort((a, b) => {
    return a.Name > b.Name ? 1 : -1;
  });

  let elementId = 'maprResultsTable' + term;

  let configId = document.getElementById("maprConfig").value;
  let linkFunc = (studyData) => {
    let type = studyData['@type'].split('#')[1].toLowerCase();
    let maprKey = configId.replace('mapr_', '');
    let maprValue = document.getElementById('maprQuery').value;
    return `/mapr/${ maprKey }/?value=${ maprValue }&show=${ type }-${ studyData['@id'] }`;
  }
  let elementSelector = `[data-id="${ elementId }"]`;

  maprData.forEach(s => renderStudy(s, elementSelector, linkFunc, maprHtml));

  // load images for each study...
  document.querySelectorAll(`[data-id="${ elementId }"] tr`).forEach(element => {
    // load children in MAPR jsTree query to get images
    let studyId = element.id;
    let objId = studyId.split("-")[1];
    let objType = studyId.split("-")[0];
    if (!objId || !objType) return;
    let childType = objType === "project" ? "datasets" : "plates";
    let configId = document.getElementById("maprConfig").value.replace('mapr_', '');
    let maprValue = term;
    // We want to link to the dataset or plate...
    let imgContainer;
    let url = `${ BASE_URL }mapr/api/${ configId }/${ childType }/?value=${ maprValue }&id=${ objId }`;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        let firstChild = data[childType][0];
        imgContainer = `${ firstChild.extra.node }-${ firstChild.id }`;
        let imagesUrl = `${ BASE_URL }mapr/api/${ configId }/images/?value=${ maprValue }&id=${ firstChild.id }&node=${ firstChild.extra.node }`;
        return fetch(imagesUrl);
      })
      .then(response => response.json())
      .then(data => {
        let html = data.images.slice(0, 3).map(i => `
          <a href="${ BASE_URL }webclient/img_detail/${ i.id }/"
             target="_blank" title="Open image in viewer" class="maprViewerLink">
            <div>
              <img class="thumbnail" src="${ STATIC_DIR }images/transparent.png"
                data-src="${ BASE_URL }webgateway/render_thumbnail/${ i.id }/">
              <i class="fas fa-eye"></i>
            </div>
          </a>`).join("");
        let linkHtml = `<a target="_blank" href="${ BASE_URL }mapr/${ configId }/?value=${ maprValue }&show=${ imgContainer }">
                  more...
                </a>`
        // Find the container and add placeholder images html
        $("#"+element.id + " .exampleImages").html(html);
        $("#"+element.id + " .exampleImagesLink").append(linkHtml);
        // Update the src to load the thumbnails. Timeout to let placeholder render while we wait for thumbs
        setTimeout(() => {
          $('img', "#"+element.id).each((index, img) => {
            img.src = img.dataset.src;
          });
        }, 0);
      });
  });
}

function render(filterFunc) {
  $('#studies').addClass('studiesLayout');
  document.getElementById('studies').innerHTML = "";

  if (!filterFunc) {
    document.getElementById('filterCount').innerHTML = "";
    return;
  }

  let studiesToRender = model.studies;
  if (filterFunc) {
    studiesToRender = model.studies.filter(filterFunc);
  }

  let filterMessage = "";
  if (studiesToRender.length === 0) {
    filterMessage = noStudiesMessage();
  } else if (studiesToRender.length < model.studies.length) {
    let configId = document.getElementById("maprConfig").value.replace('mapr_', '');
    configId = mapr_settings[configId] || configId;
    let maprValue = document.getElementById('maprQuery').value;
    filterMessage = `<p class="filterMessage">
      Found <strong>${ studiesToRender.length }</strong> studies with
      <strong>${configId}</strong>: <strong>${maprValue}</strong></p>`;
  }
  document.getElementById('filterCount').innerHTML = filterMessage;

  // By default, we link to the study itself in IDR...
  let linkFunc = (studyData) => {
    let type = studyData['@type'].split('#')[1].toLowerCase();
    return `${ BASE_URL }webclient/?show=${ type }-${ studyData['@id'] }`;
  }
  let htmlFunc = studyHtml;

  studiesToRender.forEach(s => renderStudy(s, '#studies', linkFunc, htmlFunc));

  loadStudyThumbnails();
}


// When no studies match the filter, show message/link.
function noStudiesMessage() {
  let filterMessage = "No matching studies.";
  if (SUPER_CATEGORY) {
    let currLabel = SUPER_CATEGORY.label;
    let configId = document.getElementById("maprConfig").value;
    let maprQuery = document.getElementById("maprQuery").value;
    let others = [];
    for (cat in SUPER_CATEGORIES) {
      if (SUPER_CATEGORIES[cat].label !== currLabel) {
        others.push(`<a href="${GALLERY_INDEX}${ cat }/search/?query=${configId}:${maprQuery}">${ SUPER_CATEGORIES[cat].label }</a>`);
      }
    }
    if (others.length > 0) {
      filterMessage += " Try " + others.join (" or ");
    }
  }
  return filterMessage;
}


function renderStudy(studyData, elementSelector, linkFunc, htmlFunc) {

  // Add Project or Screen to the page
  let title;
  for (let i=0; i<TITLE_KEYS.length; i++) {
    title = model.getStudyValue(studyData, TITLE_KEYS[i]);
    if (title) {
      break;
    }
  }
  if (!title) {
    title = studyData.Name;
  }
  let type = studyData['@type'].split('#')[1].toLowerCase();
  let studyLink = linkFunc(studyData);
  // save for later
  studyData.title = title;

  let desc = studyData.Description;
  let studyDesc;
  if (desc) {
    // If description contains title, use the text that follows
    if (title.length > 0 && desc.indexOf(title) > -1) {
      desc = desc.split(title)[1];
    }
    // Remove blank lines (and first 'Experiment Description' line)
    studyDesc = desc.split('\n')
      .filter(l => l.length > 0)
      .filter(l => l !== 'Experiment Description' && l !== 'Screen Description')
      .join('\n');
  }

  let idrId = studyData.Name.split('-')[0];  // idr0001
  let authors = model.getStudyValue(studyData, "Publication Authors") || "";

  let div = htmlFunc({studyLink, studyDesc, idrId, title, authors, BASE_URL, type}, studyData);
  document.querySelector(elementSelector).appendChild(div);
}

// --------- Render utils -----------
function loadStudyThumbnails() {

  let ids = [];
  // Collect study IDs 'project-1', 'screen-2' etc
  document.querySelectorAll('div.study').forEach(element => {
    let obj_id = element.dataset.obj_id;
    let obj_type = element.dataset.obj_type;
    if (obj_id && obj_type) {
      ids.push(obj_type + '-' + obj_id);
    }
  });

  // Load images
  model.loadStudiesThumbnails(ids, (data) => {
    // data is e.g. { project-1: {thumbnail: base64data, image: {id:1}} }
    for (id in data) {
      if (!data[id]) continue;  // may be null
      let obj_type = id.split('-')[0];
      let obj_id = id.split('-')[1];
      let elements = document.querySelectorAll(`div[data-obj_type="${obj_type}"][data-obj_id="${obj_id}"]`);
      for (let e=0; e<elements.length; e++) {
        // Find all studies matching the study ID and set src on image
        let element = elements[e];
        let studyImage = element.querySelector('.studyImage');
        if (data[id].thumbnail) {
          studyImage.style.backgroundImage = `url(${ data[id].thumbnail })`;
        }
        // viewer link
        if (data[id].image && data[id].image.id) {
          let iid = data[id].image.id;
          let link = `${ BASE_URL }webclient/img_detail/${ iid }/`;
          element.querySelector('a.viewerLink').href = link;
        }
      }
    }
  });
}

// ----------- Load / Filter Studies --------------------

// Do the loading and render() when done...
model.loadStudies(() => {
  // Immediately filter by Super category
  if (SUPER_CATEGORY && SUPER_CATEGORY.query) {
    model.studies = model.filterStudiesByMapQuery(SUPER_CATEGORY.query);
  }
  filterAndRender();
});

// Handle browser Back and Forwards - redo filtering
window.onpopstate = (event) => {
  populateInputsFromSearch();
  filterAndRender();
}


// Load MAPR config
fetch(BASE_URL + 'mapr/api/config/')
  .then(response => response.json())
  .then(data => {
    mapr_settings = data;

    let html = FILTER_MAPR_KEYS.map(key => {
      let config = mapr_settings[key];
      if (config) {
        return `<option value="mapr_${ key }">${ config.label }</option>`;
      } else {
        return "";
      }
    }).join("\n");
    document.getElementById('maprKeys').innerHTML = html;

    populateInputsFromSearch();
  });
