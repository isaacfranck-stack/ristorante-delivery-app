export default function Privacy() {
  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
      <p className="mb-4">La tua privacy è importante per noi. Questa pagina descrive come raccogliamo, utilizziamo e proteggiamo i tuoi dati personali.</p>
      <h2 className="text-xl font-semibold mt-6 mb-2">Dati raccolti</h2>
      <ul className="list-disc ml-6 mb-4">
        <li>Dati forniti volontariamente (es. nome, email, indirizzo per la consegna)</li>
        <li>Dati raccolti automaticamente (es. dati tecnici, cookie)</li>
      </ul>
      <h2 className="text-xl font-semibold mt-6 mb-2">Utilizzo dei dati</h2>
      <ul className="list-disc ml-6 mb-4">
        <li>Gestione degli ordini e consegne</li>
        <li>Comunicazioni relative al servizio</li>
        <li>Analisi statistiche anonime</li>
      </ul>
      <p>Per richieste o informazioni sulla privacy, contattaci tramite i canali ufficiali indicati sul sito.</p>
    </div>
  );
}