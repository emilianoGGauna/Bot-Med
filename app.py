from flask import Flask, render_template, redirect, url_for, request, session
from logic import *
from utils import *

app = Flask(__name__)
app.secret_key = 'a4d5b4e2c3f8a9d0a3c5b1f9a6d8c7e5'
# Knowledge base setup
clauses = []

############################################# Enfermedades

# Enfermedades gastrointestinales
clauses.append(expr("Vomito(x) & DificultadDefecar(x) & Acidez(x) & Estrenimiento ==> Enfermo(x, ObstruccionAbdominal)"))
clauses.append(expr("Vomito(x) & Nauseas(x) & DolorAbdominal(x) & SensacionHambre(x) & Acidez(x) ==> Enfermo(x, UlceraPeptica)"))
clauses.append(expr("Nauseas(x) & DolorAbdominal(x) & DolorDefecacion(x) ==> Enfermo(x, SindromeIntestinoIrritable)"))
clauses.append(expr("Vomito(x) & Diarrea(x) & DolorAbdominal(x) & Fiebre(x) & Deshidratacion(x) ==> Enfermo(x, Gastroenteritis)"))
clauses.append(expr("Nauseas(x) & Vomito(x) & DolorAbdominal(x) & Fiebre(x) & Escalofrios(x) & Estrenimiento(x) ==> Enfermo(x, Peritonitis)"))

# Enfermedades respiratorias
clauses.append(expr("Escalofrios(x) & DolorMuscular(x) & Fiebre(x) & DolorCabeza(x)==> Enfermo(x, Influenza)"))
clauses.append(expr("DolorCabeza(x) & PerdidaOlor(x) & PerdidaGusto(x) & DificultadRespirar(x) ==> Enfermo(x, Covid)"))
clauses.append(expr("Ronquera(x) & TosSeca(x) & InflamacionCV (x) ==> Enfermo(x, Laringitis)"))
clauses.append(expr("DolorFacial(x) & SensibilidadFacial(x) ==> Enfermo(x, Sinusitis)"))
clauses.append(expr("DolorFacial(x) ==> Enfermo(x, Sinusitis)"))
clauses.append(expr("SensibilidadFacial(x) ==> Enfermo(x, Sinusitis)"))

# Enfermedades de transmisión sexual
clauses.append(expr("VerrugasGenitales(x) & VerrugasAno(x) & ArdorGenitales(x) ==> Enfermo(x, Vph)"))
clauses.append(expr("UlceraIndolora(x) & Fiebre(x) & Fatiga(x) & DolorMuscular(x) & ErupcionesPiel(x) ==> Enfermo(x, Sifilis)"))
clauses.append(expr("UlceraIndolora(x) & ErupcionesPiel ==> Enfermo(x, Sifilis)"))
clauses.append(expr("Fiebre(x) & Fatiga(x) & DolorMuscular(x) & DolorCabeza(x) & ErupcionesPiel(x) ==> Enfermo(x, Vih)"))

# Bases del arbol
sintomas = ["Fiebre", "Vomito", "Nauseas", "DolorAbdominal", "DolorMuscular", "DolorCabeza", "Fatiga", "ErupcionesPiel", "DificultadDefecar", "Acidez", "Estrenimiento", "SensacionHambre", "DolorDefecacion", "Diarrea", "Deshidratacion", "Escalofrios", "PerdidaOlor", "PerdidaGusto", "DificultadRespirar", "Ronquera", "TosSeca", "InflamacionCV", "DolorFacial", "SensibilidadFacial", "VerrugasGenitales", "VerrugasAno", "ArdorGenitales", "UlceraIndolora"]
relaciones = {
    "Vomito": ["Nauseas", "DificultadDefecar", "Acidez", "Estrenimiento", "DolorAbdominal", "SensacionHambre", "Diarrea", "Fiebre", "Deshidratacion", "Escalofrios"],
    "Nauseas": ["Vomito", "DolorAbdominal", "SensacionHambre", "Acidez", "DolorDefecacion", "Fiebre", "Escalofrios", "Estrenimiento", 'Diarrea'],
    "DolorAbdominal": ["Vomito", "Nauseas", "SensacionHambre", "Acidez", "DolorDefecacion", "Fiebre", "Deshidratacion", "Escalofrios", "Estrenimiento", 'Diarrea'],
    "DolorCabeza": ["Escalofrios", "DolorMuscular", "Fiebre", "PerdidaOlor", "PerdidaGusto", "DificultadRespirar", "Fatiga", "ErupcionesPiel"],
    "Fiebre": ["Fatiga", "DolorMuscular", "DolorCabeza", "ErupcionesPiel", "UlceraIndolora", "ErupcionesPiel", "Vomito", "Diarrea", "DolorAbdominal", "Deshidratacion", "Nauseas", "Vomito", "Escalofrios", "Estrenimiento"],
    "Fatiga": ["Fiebre", "DolorMuscular", "DolorCabeza", "ErupcionesPiel", "UlceraIndolora"],
    "ErupcionesPiel": ["Fiebre", "Fatiga", "DolorMuscular", "DolorCabeza", "UlceraIndolora"],
    "DolorMuscular": ["Escalofrios", "DolorCabeza", "Fiebre", "ErupcionesPiel", "UlceraIndolora", "Fatiga",]
}


############ Tratamientos para enfermedades

# gastrointestinales
clauses.append(expr("Enfermo(x, ObstruccionAbdominal) ==> Tratamiento(NPO, x)"))
clauses.append(expr("Enfermo(x, ObstruccionAbdominal) ==> Tratamiento(IVFluids, x)"))
clauses.append(expr("Enfermo(x, ObstruccionAbdominal) ==> Tratamiento(ReposicionElectrolitos, x)"))
clauses.append(expr("Enfermo(x, ObstruccionAbdominal) ==> Tratamiento(AntibioticosEmpiricos, x)"))
clauses.append(expr("Enfermo(x, UlceraPeptica) ==> Tratamiento(IBP, x)"))
clauses.append(expr("Enfermo(x, UlceraPeptica) ==> Tratamiento(BloqueadoresH2, x)"))
clauses.append(expr("Enfermo(x, UlceraPeptica) ==> Tratamiento(Antiacidos, x)"))
clauses.append(expr("Enfermo(x, UlceraPeptica) ==> Tratamiento(Antibioticos, x)"))
clauses.append(expr("Enfermo(x, SindromeIntestinoIrritable) ==> Tratamiento(CambiosEstiloVida, x)"))
clauses.append(expr("Enfermo(x, SindromeIntestinoIrritable) ==> Tratamiento(TerapiaPsicoconductual, x)"))
clauses.append(expr("Enfermo(x, SindromeIntestinoIrritable) ==> Tratamiento(Medicamentos, x)"))
clauses.append(expr("Enfermo(x, Gastroenteritis) ==> Tratamiento(TerapiaApoyo, x)"))
clauses.append(expr("Enfermo(x, Gastroenteritis) ==> Tratamiento(ConsultaUnMedico, x)"))
clauses.append(expr("Enfermo(x, Peritonitis) ==> Tratamiento(AntibioticosPeritonitis, x)"))
clauses.append(expr("Enfermo(x, Peritonitis) ==> Tratamiento(Analgesicos, x)"))
clauses.append(expr("Enfermo(x, Peritonitis) ==> Tratamiento(ReposicionElectrolitos, x)"))

# respiratorias
clauses.append(expr("Enfermo(x, Influenza) ==> Tratamiento(TerapiaAntiviral, x)"))
clauses.append(expr("Enfermo(x, Covid) ==> Tratamiento(TerapiaAntiviral, x)"))
clauses.append(expr("Enfermo(x, Covid) ==> Tratamiento(Corticosteroides, x)"))
clauses.append(expr("Enfermo(x, Laringitis) ==> Tratamiento(Amoxicilina, x)"))
clauses.append(expr("Enfermo(x, Sinusitis) ==> Tratamiento(Amoxicilina, x)"))

# ETS
clauses.append(expr("Enfermo(x, Vph) ==> Tratamiento(MonitoreoClinico, x)"))
clauses.append(expr("Enfermo(x, Vph) ==> Tratamiento(Podofilotoxina, x)"))
clauses.append(expr("Enfermo(x, Vph) ==> Tratamiento(ExtirpacionQuirurjica, x)"))
clauses.append(expr("Enfermo(x, Sifilis) ==> Tratamiento(Penicilina, x)"))
clauses.append(expr("Enfermo(x, Sifilis) ==> Tratamiento(DosisIm, x)"))
clauses.append(expr("Enfermo(x, Sifilis) ==> Tratamiento(Doxicilina, x)"))
clauses.append(expr("Enfermo(x, Vih) ==> Tratamiento(Didanosina, x)"))
clauses.append(expr("Enfermo(x, Vih) ==> Tratamiento(Emtricitabina, x)"))
clauses.append(expr("Enfermo(x, Vih) ==> Tratamiento(Tenofovir, x)"))

# Tratamientos para algunos sintomas
clauses.append(expr("DolorCabeza(x) ==> Tratamiento(Tempra, x)"))

# Base de conocimiento
kb = FolKB(clauses)

# Initialize patient information
patient_name = ""


@app.route("/", methods=["GET", "POST"])
def index():
    global patient_name, sintomas, diagnosis, treatment
    
    if request.method == "POST":
        patient_name = request.form.get("patient_name")
        return redirect(url_for("questions"))

    return render_template("index.html")

@app.route("/questions", methods=["GET", "POST"])
def questions():
    global sintomas, patient_name, kb

    if request.method == "POST":
        pop = True
        answer = request.form.get("answer")
        symptom = sintomas[0]

        if answer == "yes":
            kb.tell(expr(f"{symptom}({patient_name})"))
            if symptom in relaciones:
                actual = set(sintomas)
                sintomas = [x for x in relaciones[symptom] if x in actual]
                pop = False
        if pop:
            sintomas.pop(0)

        if len(sintomas) == 0:
            return redirect(url_for("results"))

    if len(sintomas) > 0:
        return render_template("questions.html", symptom=sintomas[0])
    else:
        return redirect(url_for("results"))

@app.route("/results")
def results():
    global kb, patient_name
 
    diagnosis = fol_fc_ask(kb, expr("Enfermo({}, x)".format(patient_name)))
    diagnosis = list(diagnosis)
    for idx, item in enumerate(diagnosis):
        diagnosis[idx] = f'{patient_name}: {item[x]}'

    treatment = fol_fc_ask(kb, expr("Tratamiento(x, {})".format(patient_name)))
    treatment = list(treatment)
    for idx, item in enumerate(treatment):
        treatment[idx] = f'{item[x]}'
        
    return render_template("results.html", diagnosis=diagnosis, treatment=treatment)
    
    
if __name__ == "__main__":
    app.run(debug=True)