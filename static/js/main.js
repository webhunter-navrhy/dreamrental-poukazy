// Hlavička po odscrollování, objevování sekcí, pás flotily a konfigurátor poukazu.
(function () {
  var hlavicka = document.querySelector('.hlavicka');
  function scroll() { hlavicka.classList.toggle('je-scroll', window.scrollY > 20); }
  scroll();
  window.addEventListener('scroll', scroll, { passive: true });

  // objevování: jen když prohlížeč umí IntersectionObserver a uživatel nechce omezit pohyb
  var klid = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !klid) {
    var io = new IntersectionObserver(function (zaznamy) {
      zaznamy.forEach(function (z) { if (z.isIntersecting) { z.target.classList.add('je-videt'); io.unobserve(z.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.sekce__hlava, .darek, .karta, .pole, .souhrn, .kroky li, .auto, .recenze__karta, .otazky__seznam, .brana__text').forEach(function (el) {
      if (el.getBoundingClientRect().top > window.innerHeight) { el.classList.add('objev'); io.observe(el); }
    });
  }

  // flotila: šipky posouvají pás o kartu
  var pas = document.querySelector('.flotila__pas');
  document.querySelectorAll('[data-posun]').forEach(function (b) {
    b.addEventListener('click', function () {
      var karta = pas.querySelector('.auto');
      pas.scrollBy({ left: (karta.offsetWidth + 16) * 2 * Number(b.dataset.posun), behavior: 'smooth' });
    });
  });

  // KONFIGURÁTOR
  var f = document.getElementById('formular');
  if (!f) return;
  var karta = document.getElementById('karta');
  var k = function (n) { return karta.querySelector('[data-k="' + n + '"]'); };
  var s = function (n) { return f.querySelector('[data-s="' + n + '"]'); };
  var poptat = document.getElementById('poptat');
  var adresa = poptat.getAttribute('href').replace('mailto:', '');
  var poleCastka = f.querySelector('.pole__castka');
  var kc = function (n) { return Math.round(n).toLocaleString('cs-CZ').replace(/\s/g, ' ') + ' Kč'; };

  function darek() { return f.querySelector('input[name="darek"]:checked'); }
  function pocet() {
    var n = parseInt(f.pocet.value, 10);
    return isNaN(n) || n < 1 ? 1 : Math.min(n, 999);
  }

  var posledniFoto = '';
  function prekresli() {
    var d = darek();
    var castka = d.value === 'castka';
    poleCastka.hidden = !castka;
    var hodnota = castka ? Math.max(1000, parseInt(f.castka.value, 10) || 0) : Number(d.dataset.cena);
    var nazev = castka ? 'Poukaz na ' + kc(hodnota) : d.dataset.nazev;
    k('nazev').textContent = nazev;
    k('firma').textContent = f.firma.value.trim() || 'vaší firmy';
    k('venovani').textContent = f.venovani.value.trim() || ' ';
    if (d.dataset.foto !== posledniFoto) {
      var foto = k('foto');
      posledniFoto = d.dataset.foto;
      foto.classList.add('je-zmena');
      setTimeout(function () { foto.src = posledniFoto; foto.onload = function () { foto.classList.remove('je-zmena'); }; }, 250);
    }

    var n = pocet();
    s('vzorec').textContent = n + ' × ' + kc(hodnota);
    s('celkem').textContent = kc(n * hodnota);
    if (castka) {
      s('pozn').textContent = 'Firemní slevu u poukazů na částku potvrdíme v nabídce.';
    } else {
      var uspora = (Number(d.dataset.bezne) - hodnota) * n;
      s('pozn').textContent = 'včetně DPH · oproti běžné ceně ušetříte ' + kc(uspora);
    }

    var text = [
      'Dobrý den,',
      '',
      'máme zájem o firemní vánoční poukazy DREAMRENTAL.',
      '',
      'Dárek: ' + nazev,
      'Počet poukazů: ' + n,
      'Orientační cena celkem: ' + kc(n * hodnota).replace(/ /g, ' ') + ' vč. DPH',
      'Firma: ' + (f.firma.value.trim() || '(doplníme)'),
      'Věnování: ' + (f.venovani.value.trim() || '(doplníme)'),
      '',
      'Logo pošleme v příloze.',
      '',
      'Děkujeme'
    ].join('\n');
    poptat.href = 'mailto:' + adresa + '?subject=' + encodeURIComponent('Firemní poukazy DREAMRENTAL – ' + n + ' × ' + nazev.replace(/ /g, ' ')) + '&body=' + encodeURIComponent(text);
  }

  f.addEventListener('input', prekresli);
  f.addEventListener('change', prekresli);
  f.addEventListener('submit', function (e) { e.preventDefault(); });

  f.querySelectorAll('[data-krok]').forEach(function (b) {
    b.addEventListener('click', function () { f.pocet.value = Math.max(1, Math.min(999, pocet() + Number(b.dataset.krok))); prekresli(); });
  });
  f.querySelectorAll('[data-venovani]').forEach(function (b) {
    b.addEventListener('click', function () { f.venovani.value = b.dataset.venovani; prekresli(); });
  });

  // logo jen do náhledu, nikam se neposílá
  f.logo.addEventListener('change', function () {
    var soubor = f.logo.files && f.logo.files[0];
    var img = k('logo'), text = k('logo-text');
    if (!soubor) { img.hidden = true; text.hidden = false; return; }
    var r = new FileReader();
    r.onload = function () { img.src = r.result; img.alt = 'Logo firmy'; img.hidden = false; text.hidden = true; };
    r.readAsDataURL(soubor);
  });

  // tlačítka u dárků: předvybrat dárek a sjet ke konfigurátoru
  document.querySelectorAll('[data-vybrat]').forEach(function (b) {
    b.addEventListener('click', function () {
      var r = f.querySelector('input[name="darek"][value="' + b.dataset.vybrat + '"]');
      if (r) { r.checked = true; prekresli(); }
      document.getElementById('poukaz').scrollIntoView({ behavior: klid ? 'auto' : 'smooth' });
    });
  });

  prekresli();
})();
