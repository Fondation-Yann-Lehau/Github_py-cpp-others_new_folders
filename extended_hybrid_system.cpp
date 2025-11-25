/**
 * extended_hybrid_system.cpp
 * ==========================
 * Extension complète du système hybride quantique-binaire en C++.
 * Développe les concepts de transition cycloidale, conjonction/annulation,
 * et transformation de données selon une architecture modulaire avancée.
 * 
 * Basé sur la retranscription systémique de la symbolique informatique des fichiers:
 * - HybridBinarySystem.cpp
 * - unified_robot_system.cpp
 * 
 * Environ 1000 lignes de code fonctionnel.
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <functional>
#include <chrono>
#include <thread>
#include <random>
#include <memory>
#include <stdexcept>
#include <iomanip>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <queue>
#include <optional>
#include <variant>

// =============================================================================
// SECTION 1: ÉNUMÉRATIONS ET TYPES DE BASE
// =============================================================================

namespace QuantumSymbolic {

/**
 * États binaires fondamentaux avec signification symbolique.
 */
enum class BinaryState {
    ZERO = 0,      // Annulation / Intégration / Achèvement
    ONE = 1,       // Initiation / Structuration / Activation
    UNDEFINED = -1 // État de superposition avant observation
};

/**
 * Types d'opérations logiques supportées.
 */
enum class OperationType {
    AND,    // Conjonction
    OR,     // Disjonction
    XOR,    // Annulation / Différence
    NOT,    // Négation
    NAND,   // Non-conjonction
    NOR,    // Non-disjonction
    XNOR    // Équivalence
};

/**
 * Phases de transition quantique-classique.
 */
enum class TransitionPhase {
    WAVE,       // Onde - potentiel en mouvement
    TRANSITION, // Transition cycloïdale
    COLLAPSE,   // Effondrement vers état fixe
    FIXED       // État binaire déterminé
};

/**
 * Décisions de navigation possibles.
 */
enum class NavigationDecision {
    FORWARD,
    TURN_LEFT,
    TURN_RIGHT,
    REVERSE,
    STOP
};

/**
 * Convertit une opération en chaîne lisible.
 */
std::string operationToString(OperationType op) {
    switch (op) {
        case OperationType::AND:  return "AND (∧)";
        case OperationType::OR:   return "OR (∨)";
        case OperationType::XOR:  return "XOR (⊕)";
        case OperationType::NOT:  return "NOT (¬)";
        case OperationType::NAND: return "NAND (⊼)";
        case OperationType::NOR:  return "NOR (⊽)";
        case OperationType::XNOR: return "XNOR (⊙)";
        default: return "UNKNOWN";
    }
}

/**
 * Convertit une décision de navigation en chaîne.
 */
std::string decisionToString(NavigationDecision d) {
    switch (d) {
        case NavigationDecision::FORWARD:    return "FORWARD";
        case NavigationDecision::TURN_LEFT:  return "TURN_LEFT";
        case NavigationDecision::TURN_RIGHT: return "TURN_RIGHT";
        case NavigationDecision::REVERSE:    return "REVERSE";
        case NavigationDecision::STOP:       return "STOP";
        default: return "UNKNOWN";
    }
}

// =============================================================================
// SECTION 2: STRUCTURES DE DONNÉES
// =============================================================================

/**
 * Représente une observation dans le système quantique symbolique.
 */
struct QuantumObservation {
    std::string context;
    bool potentialState;
    std::optional<bool> observedState;
    TransitionPhase phase = TransitionPhase::WAVE;
    std::chrono::system_clock::time_point timestamp;
    
    QuantumObservation(const std::string& ctx, bool potential)
        : context(ctx), potentialState(potential), 
          timestamp(std::chrono::system_clock::now()) {}
    
    bool collapse() {
        observedState = potentialState;
        phase = TransitionPhase::FIXED;
        return *observedState;
    }
};

/**
 * Résultat d'une opération logique.
 */
struct OperationResult {
    OperationType operation;
    std::vector<bool> inputs;
    bool rawResult;
    std::optional<bool> collapsedResult;
    double executionTimeMs = 0.0;
    std::string context;
};

/**
 * Données d'un capteur simulé.
 */
struct SensorReading {
    std::string name;
    double value;
    std::chrono::system_clock::time_point timestamp;
};

// =============================================================================
// SECTION 3: MOTEUR DE VISUALISATION
// =============================================================================

/**
 * Moteur de visualisation des transitions quantique-classique.
 */
class VisualizationEngine {
private:
    int delayMs;
    bool enabled;
    
    void sleep(int ms) const {
        std::this_thread::sleep_for(std::chrono::milliseconds(ms));
    }
    
public:
    explicit VisualizationEngine(int delay = 150, bool enable = true)
        : delayMs(delay), enabled(enable) {}
    
    void setEnabled(bool enable) { enabled = enable; }
    
    /**
     * Visualise l'effondrement d'un état quantique.
     */
    void visualizeCollapse(BinaryState state) const {
        if (!enabled) return;
        
        bool finalState = (state == BinaryState::ONE);
        
        std::cout << " | Traitement: ";
        std::cout.flush();
        
        // Phase 1: Onde
        std::cout << "~ ~ ~ (ONDE) ";
        std::cout.flush();
        sleep(delayMs);
        
        std::cout << "→ ";
        std::cout.flush();
        sleep(delayMs);
        
        // Phase 2: Transition
        std::cout << "(•) (TRANSITION) ";
        std::cout.flush();
        sleep(delayMs);
        
        std::cout << "→ ";
        std::cout.flush();
        sleep(delayMs);
        
        // Phase 3: État fixé
        if (finalState) {
            std::cout << "[ 1 ] (CRISTALLISÉ)" << std::endl;
        } else {
            std::cout << "[ 0 ] (ANNULÉ)" << std::endl;
        }
        std::cout << std::string(50, '-') << std::endl;
    }
    
    /**
     * Visualise le résultat d'une opération logique.
     */
    void visualizeOperation(OperationType op, bool result) const {
        if (!enabled) return;
        std::cout << "  [" << operationToString(op) << "] Résultat: " 
                  << (result ? 1 : 0) << std::endl;
    }
    
    /**
     * Visualise un flux de données.
     */
    void visualizeDataFlow(const std::vector<double>& data, 
                          const std::string& label = "Flux") const {
        if (!enabled || data.empty()) return;
        
        double maxVal = *std::max_element(data.begin(), data.end(),
            [](double a, double b) { return std::abs(a) < std::abs(b); });
        maxVal = std::abs(maxVal);
        if (maxVal == 0) maxVal = 1;
        
        std::cout << "\n[" << label << "] Visualisation:" << std::endl;
        
        size_t limit = std::min(data.size(), static_cast<size_t>(10));
        for (size_t i = 0; i < limit; ++i) {
            int normalized = static_cast<int>(20 * std::abs(data[i]) / maxVal);
            std::string bar(normalized, '#');
            std::cout << "  [" << std::setw(2) << std::setfill('0') << i << "] "
                      << std::setw(20) << std::setfill(' ') << std::left << bar
                      << " " << std::scientific << std::setprecision(2) 
                      << data[i] << std::endl;
        }
    }
};

// =============================================================================
// SECTION 4: PONT QUANTIQUE-CLASSIQUE
// =============================================================================

/**
 * Pont métaphorique entre le monde quantique (potentiel) et classique (déterminé).
 */
class QuantumClassicalBridge {
private:
    std::shared_ptr<VisualizationEngine> viz;
    int transitionCount = 0;
    std::vector<QuantumObservation> observations;
    
    const std::string paradigmDescription = R"(
============================================================
PONT QUANTIQUE-CLASSIQUE INITIALISÉ
============================================================
Paradigme: États binaires comme transitions cycloïdales
  - État |1⟩: Initiation / Structuration
  - État |0⟩: Intégration / Achèvement
  - Superposition: Potentiel avant observation
============================================================
)";
    
public:
    explicit QuantumClassicalBridge(std::shared_ptr<VisualizationEngine> v = nullptr)
        : viz(v ? v : std::make_shared<VisualizationEngine>()) {}
    
    /**
     * Affiche la description du paradigme.
     */
    void describeParadigm() const {
        std::cout << paradigmDescription << std::endl;
    }
    
    /**
     * Visualise une transition d'état.
     */
    void visualizeTransition(bool state) const {
        BinaryState binaryState = state ? BinaryState::ONE : BinaryState::ZERO;
        viz->visualizeCollapse(binaryState);
    }
    
    /**
     * Interprète un état potentiel en état classique déterminé.
     */
    bool interpretState(bool potential, const std::string& context) {
        ++transitionCount;
        
        QuantumObservation obs(context, potential);
        
        std::cout << "\n[OBSERVATION #" << transitionCount << "] Contexte: " 
                  << context << std::endl;
        
        obs.phase = TransitionPhase::TRANSITION;
        visualizeTransition(potential);
        
        bool finalState = obs.collapse();
        observations.push_back(obs);
        
        return finalState;
    }
    
    int getTransitionCount() const { return transitionCount; }
    
    /**
     * Retourne un résumé des observations.
     */
    std::map<std::string, int> getObservationsSummary() const {
        std::map<std::string, int> summary;
        summary["total"] = static_cast<int>(observations.size());
        summary["ones"] = static_cast<int>(std::count_if(observations.begin(), 
            observations.end(), [](const QuantumObservation& o) {
                return o.observedState.value_or(false);
            }));
        summary["zeros"] = summary["total"] - summary["ones"];
        return summary;
    }
};

// =============================================================================
// SECTION 5: PROCESSEUR D'OPÉRATIONS LOGIQUES
// =============================================================================

/**
 * Processeur d'opérations logiques avec support quantique symbolique.
 */
class LogicProcessor {
private:
    std::shared_ptr<QuantumClassicalBridge> bridge;
    std::shared_ptr<VisualizationEngine> viz;
    std::map<OperationType, int> operationCounts;
    double totalExecutionTimeMs = 0.0;
    std::vector<OperationResult> resultsHistory;
    
    /**
     * Calcule le résultat brut d'une opération.
     */
    bool computeOperation(OperationType op, const std::vector<bool>& inputs) {
        if (inputs.empty()) {
            throw std::invalid_argument("Aucune entrée fournie");
        }
        
        switch (op) {
            case OperationType::AND: {
                return std::all_of(inputs.begin(), inputs.end(), 
                    [](bool b) { return b; });
            }
            case OperationType::OR: {
                return std::any_of(inputs.begin(), inputs.end(), 
                    [](bool b) { return b; });
            }
            case OperationType::XOR: {
                int count = std::count(inputs.begin(), inputs.end(), true);
                return count % 2 == 1;
            }
            case OperationType::NOT: {
                return !inputs[0];
            }
            case OperationType::NAND: {
                return !std::all_of(inputs.begin(), inputs.end(), 
                    [](bool b) { return b; });
            }
            case OperationType::NOR: {
                return !std::any_of(inputs.begin(), inputs.end(), 
                    [](bool b) { return b; });
            }
            case OperationType::XNOR: {
                int count = std::count(inputs.begin(), inputs.end(), true);
                return count % 2 == 0;
            }
            default:
                throw std::invalid_argument("Opération non supportée");
        }
    }
    
public:
    LogicProcessor(std::shared_ptr<QuantumClassicalBridge> b,
                   std::shared_ptr<VisualizationEngine> v = nullptr)
        : bridge(b), viz(v ? v : std::make_shared<VisualizationEngine>()) {}
    
    /**
     * Exécute une opération logique avec passage par le pont quantique.
     */
    OperationResult execute(OperationType operation, 
                           const std::vector<bool>& inputs,
                           const std::string& context = "") {
        auto startTime = std::chrono::high_resolution_clock::now();
        
        // Calcul du résultat brut
        bool rawResult = computeOperation(operation, inputs);
        
        // Visualisation de l'opération
        viz->visualizeOperation(operation, rawResult);
        
        // Passage par le pont quantique
        std::string fullContext = context.empty() ? 
            operationToString(operation) : 
            operationToString(operation) + ": " + context;
        bool collapsedResult = bridge->interpretState(rawResult, fullContext);
        
        // Calcul du temps d'exécution
        auto endTime = std::chrono::high_resolution_clock::now();
        double executionTime = std::chrono::duration<double, std::milli>(
            endTime - startTime).count();
        totalExecutionTimeMs += executionTime;
        
        // Création du résultat
        OperationResult result;
        result.operation = operation;
        result.inputs = inputs;
        result.rawResult = rawResult;
        result.collapsedResult = collapsedResult;
        result.executionTimeMs = executionTime;
        result.context = fullContext;
        
        // Mise à jour des statistiques
        operationCounts[operation]++;
        resultsHistory.push_back(result);
        
        return result;
    }
    
    /**
     * Retourne les statistiques du processeur.
     */
    std::map<std::string, double> getStatistics() const {
        std::map<std::string, double> stats;
        int totalOps = 0;
        for (const auto& pair : operationCounts) {
            totalOps += pair.second;
        }
        stats["total_operations"] = static_cast<double>(totalOps);
        stats["total_execution_time_ms"] = totalExecutionTimeMs;
        stats["average_execution_time_ms"] = totalOps > 0 ? 
            totalExecutionTimeMs / totalOps : 0;
        return stats;
    }
};

// =============================================================================
// SECTION 6: TRANSFORMATEUR DE DONNÉES
// =============================================================================

/**
 * Transformateur de données utilisant des transformations exponentielles.
 */
class ExponentialDataTransformer {
private:
    double securityCoefficient;
    int transformationsCount = 0;
    
public:
    explicit ExponentialDataTransformer(double coeff = 0.873)
        : securityCoefficient(coeff) {}
    
    /**
     * Applique une transformation exponentielle aux caractères de la chaîne.
     */
    std::vector<double> transform(const std::string& data) {
        std::vector<double> transformed;
        transformed.reserve(data.size());
        
        for (unsigned char c : data) {
            try {
                double val = std::exp(static_cast<double>(c) * 
                    securityCoefficient / 100.0);
                transformed.push_back(val);
            } catch (...) {
                transformed.push_back(std::numeric_limits<double>::infinity());
            }
        }
        
        ++transformationsCount;
        return transformed;
    }
    
    /**
     * Tente de reconstruire les données originales.
     */
    std::string inverseTransform(const std::vector<double>& data) {
        std::string result;
        result.reserve(data.size());
        
        for (double val : data) {
            if (std::isinf(val) || val <= 0) {
                result.push_back('\0');
            } else {
                int byteVal = static_cast<int>(
                    std::log(val) * 100.0 / securityCoefficient);
                byteVal = std::max(0, std::min(255, byteVal));
                result.push_back(static_cast<char>(byteVal));
            }
        }
        
        return result;
    }
    
    int getTransformationsCount() const { return transformationsCount; }
};

// =============================================================================
// SECTION 7: QUANTIFICATEUR DE FACTEURS ABSTRAITS
// =============================================================================

/**
 * Quantifie des facteurs abstraits/symboliques en valeurs numériques.
 */
class AbstractFactorQuantifier {
private:
    double securityCoefficient;
    std::map<std::string, double> factorsMap;
    std::vector<std::map<std::string, double>> computedSignatures;
    
public:
    explicit AbstractFactorQuantifier(double coeff = 0.873)
        : securityCoefficient(coeff) {
        // Initialisation des facteurs de base
        factorsMap["stability"] = 2.342e-8;
        factorsMap["entropy"] = 9.412e-5;
        factorsMap["harmony"] = 3.1415926535;
        factorsMap["complexity"] = 11.0901;
        factorsMap["resonance"] = 1.618033988749;   // Nombre d'or
        factorsMap["coherence"] = 2.718281828;      // e
        factorsMap["balance"] = 1.41421356237;      // √2
        factorsMap["flow"] = 0.577215664901;        // Constante d'Euler-Mascheroni
    }
    
    /**
     * Quantifie les facteurs selon le coefficient de sécurité.
     */
    std::map<std::string, double> quantify() {
        std::map<std::string, double> quantified;
        for (const auto& pair : factorsMap) {
            quantified[pair.first] = pair.second * securityCoefficient;
        }
        computedSignatures.push_back(quantified);
        return quantified;
    }
    
    /**
     * Ajoute un facteur personnalisé.
     */
    void addCustomFactor(const std::string& name, double baseValue) {
        factorsMap[name] = baseValue;
    }
    
    const std::vector<std::map<std::string, double>>& getAllSignatures() const {
        return computedSignatures;
    }
};

// =============================================================================
// SECTION 8: SIMULATEUR DE CAPTEURS
// =============================================================================

/**
 * Simule des capteurs avec génération de valeurs aléatoires.
 */
class SensorSimulator {
private:
    std::string name;
    double minVal;
    double maxVal;
    std::vector<double> readings;
    std::mt19937 rng;
    std::uniform_real_distribution<double> dist;
    
public:
    SensorSimulator(const std::string& n, double min = 0, double max = 400)
        : name(n), minVal(min), maxVal(max),
          rng(std::random_device{}()), dist(min, max) {}
    
    void setSeed(unsigned int seed) { rng.seed(seed); }
    
    /**
     * Effectue une lecture du capteur.
     */
    double read() {
        double value = dist(rng);
        readings.push_back(value);
        return value;
    }
    
    /**
     * Effectue n lectures.
     */
    std::vector<double> readN(int n) {
        std::vector<double> results;
        results.reserve(n);
        for (int i = 0; i < n; ++i) {
            results.push_back(read());
        }
        return results;
    }
    
    /**
     * Retourne la moyenne des lectures.
     */
    double getAverage() const {
        if (readings.empty()) return 0;
        double sum = 0;
        for (double r : readings) sum += r;
        return sum / readings.size();
    }
    
    /**
     * Retourne les statistiques des lectures.
     */
    std::map<std::string, double> getStatistics() const {
        std::map<std::string, double> stats;
        stats["count"] = static_cast<double>(readings.size());
        
        if (readings.empty()) {
            stats["min"] = 0;
            stats["max"] = 0;
            stats["avg"] = 0;
            stats["std"] = 0;
            return stats;
        }
        
        stats["min"] = *std::min_element(readings.begin(), readings.end());
        stats["max"] = *std::max_element(readings.begin(), readings.end());
        stats["avg"] = getAverage();
        
        double variance = 0;
        double avg = stats["avg"];
        for (double r : readings) {
            variance += (r - avg) * (r - avg);
        }
        variance /= readings.size();
        stats["std"] = std::sqrt(variance);
        
        return stats;
    }
};

// =============================================================================
// SECTION 9: SIMULATEUR D'ACTIONNEURS
// =============================================================================

/**
 * Simule des actionneurs avec contrôle d'état.
 */
class ActuatorSimulator {
private:
    std::string name;
    double minState;
    double maxState;
    double currentState = 0.0;
    bool isActive = false;
    std::vector<std::pair<std::chrono::system_clock::time_point, double>> stateHistory;
    
public:
    ActuatorSimulator(const std::string& n, double min = 0, double max = 100)
        : name(n), minState(min), maxState(max) {}
    
    /**
     * Définit l'état de l'actionneur.
     */
    void setState(double value) {
        currentState = std::max(minState, std::min(maxState, value));
        isActive = currentState > 0;
        stateHistory.emplace_back(std::chrono::system_clock::now(), currentState);
    }
    
    void increment(double delta) { setState(currentState + delta); }
    void decrement(double delta) { setState(currentState - delta); }
    void reset() { setState(0); }
    
    double getCurrentState() const { return currentState; }
    bool getIsActive() const { return isActive; }
    
    const std::vector<std::pair<std::chrono::system_clock::time_point, double>>& 
    getHistory() const {
        return stateHistory;
    }
};

// =============================================================================
// SECTION 10: GESTIONNAIRE DE RÉSILIENCE
// =============================================================================

/**
 * Gestionnaire de résilience avec retry et fallback.
 */
class ResilienceManager {
private:
    int maxRetries;
    int retryDelayMs;
    int errorCount = 0;
    int recoveryCount = 0;
    std::vector<std::pair<std::chrono::system_clock::time_point, std::string>> errorLog;
    
public:
    ResilienceManager(int retries = 3, int delayMs = 100)
        : maxRetries(retries), retryDelayMs(delayMs) {}
    
    /**
     * Exécute une opération avec gestion de la résilience.
     */
    template<typename T>
    T executeWithResilience(std::function<T()> operation, T fallback, 
                           int maxRetriesOverride = -1) {
        int retries = maxRetriesOverride >= 0 ? maxRetriesOverride : maxRetries;
        
        for (int attempt = 0; attempt < retries; ++attempt) {
            try {
                return operation();
            } catch (const std::exception& e) {
                ++errorCount;
                errorLog.emplace_back(std::chrono::system_clock::now(), e.what());
                std::cout << "[RÉSILIENCE] Tentative " << (attempt + 1) 
                          << " échouée: " << e.what() << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(retryDelayMs));
            }
        }
        
        ++recoveryCount;
        std::cout << "[RÉSILIENCE] Utilisation de la valeur de fallback" << std::endl;
        return fallback;
    }
    
    int getErrorCount() const { return errorCount; }
    int getRecoveryCount() const { return recoveryCount; }
    
    double getErrorRate() const {
        int total = errorCount + recoveryCount;
        return total > 0 ? static_cast<double>(errorCount) / total : 0;
    }
};

// =============================================================================
// SECTION 11: SYSTÈME DE NAVIGATION SYMBOLIQUE
// =============================================================================

/**
 * Système de navigation basé sur la logique symbolique.
 */
class SymbolicNavigationSystem {
private:
    std::shared_ptr<QuantumClassicalBridge> bridge;
    std::shared_ptr<LogicProcessor> logic;
    double obstacleThreshold = 40.0;
    std::vector<NavigationDecision> navigationLog;
    
    std::map<std::string, std::unique_ptr<SensorSimulator>> sensors;
    std::map<std::string, std::unique_ptr<ActuatorSimulator>> actuators;
    
public:
    SymbolicNavigationSystem(std::shared_ptr<QuantumClassicalBridge> b,
                            std::shared_ptr<LogicProcessor> l)
        : bridge(b), logic(l) {
        // Initialisation des capteurs
        sensors["front"] = std::make_unique<SensorSimulator>("front_distance");
        sensors["left"] = std::make_unique<SensorSimulator>("left_distance");
        sensors["right"] = std::make_unique<SensorSimulator>("right_distance");
        
        // Initialisation des actionneurs
        actuators["left_motor"] = std::make_unique<ActuatorSimulator>("left_motor");
        actuators["right_motor"] = std::make_unique<ActuatorSimulator>("right_motor");
    }
    
    /**
     * Lit tous les capteurs.
     */
    std::map<std::string, double> readAllSensors() {
        std::map<std::string, double> readings;
        for (auto& pair : sensors) {
            readings[pair.first] = pair.second->read();
        }
        return readings;
    }
    
    /**
     * Évalue le chemin et retourne une décision de navigation.
     */
    NavigationDecision evaluatePath(const std::map<std::string, double>& readings) {
        bool frontClear = readings.at("front") >= obstacleThreshold;
        bool leftClear = readings.at("left") >= obstacleThreshold;
        bool rightClear = readings.at("right") >= obstacleThreshold;
        
        // Évaluation avec logique AND
        logic->execute(OperationType::AND, 
                      {frontClear, leftClear, rightClear},
                      "Évaluation complète du chemin");
        
        NavigationDecision decision;
        
        if (frontClear) {
            decision = NavigationDecision::FORWARD;
        } else {
            // Utilisation de XOR pour la décision de direction
            logic->execute(OperationType::XOR,
                          {leftClear, rightClear},
                          "Décision de direction");
            
            if (leftClear && !rightClear) {
                decision = NavigationDecision::TURN_LEFT;
            } else if (rightClear && !leftClear) {
                decision = NavigationDecision::TURN_RIGHT;
            } else if (leftClear && rightClear) {
                if (readings.at("left") > readings.at("right")) {
                    decision = NavigationDecision::TURN_LEFT;
                } else {
                    decision = NavigationDecision::TURN_RIGHT;
                }
            } else {
                decision = NavigationDecision::REVERSE;
            }
        }
        
        navigationLog.push_back(decision);
        return decision;
    }
    
    /**
     * Exécute un mouvement basé sur la décision.
     */
    void executeMovement(NavigationDecision decision) {
        std::map<NavigationDecision, std::pair<double, double>> movements = {
            {NavigationDecision::FORWARD, {80, 80}},
            {NavigationDecision::TURN_LEFT, {40, 80}},
            {NavigationDecision::TURN_RIGHT, {80, 40}},
            {NavigationDecision::REVERSE, {60, 60}},
            {NavigationDecision::STOP, {0, 0}}
        };
        
        auto [leftPower, rightPower] = movements[decision];
        actuators["left_motor"]->setState(leftPower);
        actuators["right_motor"]->setState(rightPower);
        
        std::cout << "[NAVIGATION] Exécution: " << decisionToString(decision) 
                  << std::endl;
    }
    
    /**
     * Exécute un cycle complet de navigation.
     */
    NavigationDecision runCycle() {
        auto readings = readAllSensors();
        
        std::cout << std::fixed << std::setprecision(1);
        std::cout << "\n[CAPTEURS] F:" << readings["front"]
                  << " L:" << readings["left"]
                  << " R:" << readings["right"] << std::endl;
        
        NavigationDecision decision = evaluatePath(readings);
        executeMovement(decision);
        
        return decision;
    }
    
    size_t getNavigationLogSize() const { return navigationLog.size(); }
};

// =============================================================================
// SECTION 12: SYSTÈME UNIFIÉ
// =============================================================================

/**
 * Système unifié intégrant tous les composants.
 */
class UnifiedExtendedSystem {
private:
    std::shared_ptr<VisualizationEngine> viz;
    std::shared_ptr<QuantumClassicalBridge> bridge;
    std::shared_ptr<LogicProcessor> logic;
    std::unique_ptr<ExponentialDataTransformer> transformer;
    std::unique_ptr<AbstractFactorQuantifier> quantifier;
    std::unique_ptr<ResilienceManager> resilience;
    std::unique_ptr<SymbolicNavigationSystem> navigation;
    
    std::chrono::system_clock::time_point startTime;
    
public:
    explicit UnifiedExtendedSystem(int animationDelayMs = 150) {
        std::cout << "\n" << std::string(70, '=') << std::endl;
        std::cout << "EXTENDED UNIFIED SYSTEM - INITIALISATION" << std::endl;
        std::cout << std::string(70, '=') << std::endl;
        
        // Composants de visualisation
        viz = std::make_shared<VisualizationEngine>(animationDelayMs);
        
        // Composants principaux
        bridge = std::make_shared<QuantumClassicalBridge>(viz);
        logic = std::make_shared<LogicProcessor>(bridge, viz);
        transformer = std::make_unique<ExponentialDataTransformer>();
        quantifier = std::make_unique<AbstractFactorQuantifier>();
        resilience = std::make_unique<ResilienceManager>();
        navigation = std::make_unique<SymbolicNavigationSystem>(bridge, logic);
        
        // Description du paradigme
        bridge->describeParadigm();
        
        startTime = std::chrono::system_clock::now();
        
        std::cout << "[SYSTÈME] Tous les composants initialisés" << std::endl;
        std::cout << std::string(70, '=') << "\n" << std::endl;
    }
    
    /**
     * Exécute des tests sur les opérations logiques.
     */
    void runLogicTests() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "TEST 1: OPÉRATIONS LOGIQUES" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        
        logic->execute(OperationType::AND, {true, true});
        logic->execute(OperationType::AND, {true, false});
        logic->execute(OperationType::XOR, {true, true});
        logic->execute(OperationType::XOR, {true, false});
        logic->execute(OperationType::OR, {false, false, true});
        logic->execute(OperationType::NOT, {true});
    }
    
    /**
     * Exécute des tests de transformation de données.
     */
    void runDataTransformationTests() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "TEST 2: TRANSFORMATION DE DONNÉES" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        
        std::string testData = "https://example.com/quantum-symbolic";
        auto transformed = transformer->transform(testData);
        
        std::cout << "Données d'entrée: " << testData.substr(0, 40) << "..." << std::endl;
        std::cout << "Longueur transformée: " << transformed.size() << std::endl;
        std::cout << "Premiers 5 valeurs: ";
        for (size_t i = 0; i < 5 && i < transformed.size(); ++i) {
            std::cout << std::scientific << std::setprecision(2) 
                      << transformed[i] << " ";
        }
        std::cout << std::endl;
        
        viz->visualizeDataFlow(transformed, "Transformation Exponentielle");
    }
    
    /**
     * Exécute la quantification des facteurs abstraits.
     */
    void runFactorQuantification() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "TEST 3: QUANTIFICATION DES FACTEURS" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        
        auto factors = quantifier->quantify();
        
        for (const auto& pair : factors) {
            std::cout << "  " << pair.first << ": " 
                      << std::scientific << std::setprecision(6) 
                      << pair.second << std::endl;
        }
    }
    
    /**
     * Exécute une simulation de navigation.
     */
    void runNavigationSimulation(int cycles = 3) {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "TEST 4: SIMULATION DE NAVIGATION" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        
        for (int i = 0; i < cycles; ++i) {
            std::cout << "\n--- Cycle " << (i + 1) << "/" << cycles << " ---" << std::endl;
            navigation->runCycle();
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }
    
    /**
     * Exécute des tests de résilience.
     */
    void runResilienceTests() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "TEST 5: RÉSILIENCE" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        
        // Test réussi
        auto result = resilience->executeWithResilience<std::string>(
            []() { return std::string("Succès!"); },
            std::string("Fallback")
        );
        std::cout << "Test réussi: " << result << std::endl;
        
        // Test avec échecs
        int failCounter = 0;
        auto failResult = resilience->executeWithResilience<std::string>(
            [&failCounter]() -> std::string {
                ++failCounter;
                if (failCounter < 4) {
                    throw std::runtime_error("Échec simulé");
                }
                return "Récupéré!";
            },
            std::string("Fallback utilisé"),
            3
        );
        std::cout << "Test avec échecs: " << failResult << std::endl;
    }
    
    /**
     * Affiche un rapport complet du système.
     */
    void printSystemReport() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "RAPPORT DU SYSTÈME" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        
        // Statistiques du processeur logique
        auto logicStats = logic->getStatistics();
        std::cout << "\n[Processeur Logique]" << std::endl;
        std::cout << "  Opérations totales: " 
                  << static_cast<int>(logicStats["total_operations"]) << std::endl;
        std::cout << "  Temps d'exécution total: " 
                  << std::fixed << std::setprecision(2) 
                  << logicStats["total_execution_time_ms"] << " ms" << std::endl;
        
        // Statistiques du pont quantique
        auto obsSummary = bridge->getObservationsSummary();
        std::cout << "\n[Pont Quantique-Classique]" << std::endl;
        std::cout << "  Transitions totales: " 
                  << bridge->getTransitionCount() << std::endl;
        std::cout << "  États |1⟩: " << obsSummary["ones"] << std::endl;
        std::cout << "  États |0⟩: " << obsSummary["zeros"] << std::endl;
        
        // Statistiques de résilience
        std::cout << "\n[Résilience]" << std::endl;
        std::cout << "  Erreurs: " << resilience->getErrorCount() << std::endl;
        std::cout << "  Récupérations: " << resilience->getRecoveryCount() << std::endl;
        
        // Statistiques de navigation
        std::cout << "\n[Navigation]" << std::endl;
        std::cout << "  Décisions prises: " 
                  << navigation->getNavigationLogSize() << std::endl;
        
        // Durée d'exécution
        auto endTime = std::chrono::system_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            endTime - startTime);
        std::cout << "\n[Temps d'exécution]: " 
                  << (duration.count() / 1000.0) << " secondes" << std::endl;
    }
    
    /**
     * Exécute tous les tests.
     */
    void runAllTests() {
        runLogicTests();
        runDataTransformationTests();
        runFactorQuantification();
        runNavigationSimulation(3);
        runResilienceTests();
        printSystemReport();
    }
};

} // namespace QuantumSymbolic

// =============================================================================
// SECTION 13: POINT D'ENTRÉE PRINCIPAL
// =============================================================================

int main() {
    std::cout << "\n" << std::string(70, '#') << std::endl;
    std::cout << "#" << std::string(20, ' ') 
              << "DÉMONSTRATION DU SYSTÈME" 
              << std::string(20, ' ') << "#" << std::endl;
    std::cout << std::string(70, '#') << "\n" << std::endl;
    
    // Création et exécution du système unifié
    QuantumSymbolic::UnifiedExtendedSystem system(100);
    system.runAllTests();
    
    std::cout << "\n" << std::string(70, '#') << std::endl;
    std::cout << "#" << std::string(18, ' ') 
              << "DÉMONSTRATION TERMINÉE" 
              << std::string(18, ' ') << "#" << std::endl;
    std::cout << std::string(70, '#') << "\n" << std::endl;
    
    return 0;
}
