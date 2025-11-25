/**
 * Système Robotique Unifié
 * ========================
 * Architecture technique combinant :
 * - Logique binaire classique avec transitions quantique-symbolique
 * - Navigation autonome avec architecture comportementale
 * - Communication série et Wi-Fi
 * - Gestion d'exceptions et résilience
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <functional>
#include <chrono>
#include <thread>
#include <random>
#include <memory>
#include <stdexcept>

// =============================================================================
// SECTION 1 : ÉNUMÉRATIONS ET TYPES
// =============================================================================

enum class BinaryState { ZERO = 0, ONE = 1 };

enum class OperationType { AND, OR, XOR, NOT, NAND, NOR };

enum class SystemMode { AUTONOMOUS, MANUAL, HYBRID };

enum class NavigationDecision { FORWARD, TURN_LEFT, TURN_RIGHT, REVERSE, STOP };

// =============================================================================
// SECTION 2 : UTILITAIRES
// =============================================================================

class RandomGenerator {
private:
    std::mt19937 gen;
    std::uniform_real_distribution<> dist;
public:
    RandomGenerator(double min = 0.0, double max = 400.0) 
        : gen(std::random_device{}()), dist(min, max) {}
    
    double generate() { return dist(gen); }
};

// =============================================================================
// SECTION 3 : MOTEUR DE VISUALISATION
// =============================================================================

class VisualizationEngine {
private:
    int delay_ms;
    bool enabled;

    void sleep_ms(int ms) const {
        std::this_thread::sleep_for(std::chrono::milliseconds(ms));
    }

public:
    VisualizationEngine(int delay = 150, bool enable = true) 
        : delay_ms(delay), enabled(enable) {}

    void setEnabled(bool enable) { enabled = enable; }

    void visualizeCollapse(BinaryState state) const {
        if (!enabled) return;
        
        std::cout << " | Processing: ";
        std::cout << "~ ~ ~ (WAVE) "; std::cout.flush();
        sleep_ms(delay_ms);
        
        std::cout << "-> (•) (TRANSITION) "; std::cout.flush();
        sleep_ms(delay_ms);
        
        std::cout << "-> ";
        if (state == BinaryState::ONE) {
            std::cout << "[ 1 ] (CRYSTALLIZED)" << std::endl;
        } else {
            std::cout << "[ 0 ] (ANNULLED)" << std::endl;
        }
        std::cout << std::string(50, '-') << std::endl;
    }

    void visualizeOperation(OperationType op, bool result) const {
        if (!enabled) return;
        
        static const std::map<OperationType, std::string> symbols = {
            {OperationType::AND, "AND (∧)"},
            {OperationType::OR, "OR (∨)"},
            {OperationType::XOR, "XOR (⊕)"},
            {OperationType::NOT, "NOT (¬)"},
            {OperationType::NAND, "NAND (⊼)"},
            {OperationType::NOR, "NOR (⊽)"}
        };
        
        auto it = symbols.find(op);
        std::string opName = (it != symbols.end()) ? it->second : "UNKNOWN";
        std::cout << "  [" << opName << "] Result: " << result << std::endl;
    }
};

// =============================================================================
// SECTION 4 : PONT QUANTIQUE-CLASSIQUE
// =============================================================================

class QuantumClassicalBridge {
private:
    std::shared_ptr<VisualizationEngine> viz;
    int transition_count;

public:
    QuantumClassicalBridge(std::shared_ptr<VisualizationEngine> v = nullptr)
        : viz(v ? v : std::make_shared<VisualizationEngine>()), transition_count(0) {}

    void describeParadigm() const {
        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "QUANTUM-CLASSICAL BRIDGE INITIALIZED" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        std::cout << "Paradigm: Binary states as cycloidal transitions" << std::endl;
        std::cout << "  - State |1>: Initiation/Structuration" << std::endl;
        std::cout << "  - State |0>: Integration/Completion" << std::endl;
        std::cout << std::string(60, '=') << "\n" << std::endl;
    }

    BinaryState interpretState(bool potential, const std::string& context) {
        transition_count++;
        
        std::cout << "\n[OBSERVATION #" << transition_count 
                  << "] Context: " << context << std::endl;
        
        BinaryState state = potential ? BinaryState::ONE : BinaryState::ZERO;
        viz->visualizeCollapse(state);
        
        return state;
    }

    int getTransitionCount() const { return transition_count; }
};

// =============================================================================
// SECTION 5 : PROCESSEUR D'OPÉRATIONS LOGIQUES
// =============================================================================

class LogicProcessor {
private:
    std::shared_ptr<QuantumClassicalBridge> bridge;
    std::shared_ptr<VisualizationEngine> viz;
    std::map<OperationType, int> operation_counts;

public:
    LogicProcessor(std::shared_ptr<QuantumClassicalBridge> b,
                   std::shared_ptr<VisualizationEngine> v)
        : bridge(b), viz(v) {}

    BinaryState execute(OperationType op, const std::vector<bool>& inputs,
                        const std::string& context = "") {
        if (inputs.empty()) {
            throw std::invalid_argument("No inputs provided");
        }

        bool result = false;
        
        switch (op) {
            case OperationType::AND:
                result = true;
                for (bool b : inputs) result = result && b;
                break;
            case OperationType::OR:
                result = false;
                for (bool b : inputs) result = result || b;
                break;
            case OperationType::XOR: {
                int sum = 0;
                for (bool b : inputs) sum += b ? 1 : 0;
                result = (sum % 2 == 1);
                break;
            }
            case OperationType::NOT:
                result = !inputs[0];
                break;
            case OperationType::NAND:
                result = true;
                for (bool b : inputs) result = result && b;
                result = !result;
                break;
            case OperationType::NOR:
                result = false;
                for (bool b : inputs) result = result || b;
                result = !result;
                break;
        }

        operation_counts[op]++;
        viz->visualizeOperation(op, result);
        
        std::string fullContext = context.empty() ? "Logic operation" : context;
        return bridge->interpretState(result, fullContext);
    }

    std::map<OperationType, int> getStatistics() const { return operation_counts; }
};

// =============================================================================
// SECTION 6 : SIMULATEUR DE CAPTEURS
// =============================================================================

class SensorSimulator {
private:
    std::string name;
    RandomGenerator rng;

public:
    SensorSimulator(const std::string& n, double min = 0, double max = 400)
        : name(n), rng(min, max) {}

    double read() { return rng.generate(); }
    std::string getName() const { return name; }
};

// =============================================================================
// SECTION 7 : SIMULATEUR D'ACTIONNEURS
// =============================================================================

class ActuatorSimulator {
private:
    std::string name;
    double state;
    bool active;

public:
    ActuatorSimulator(const std::string& n) : name(n), state(0), active(false) {}

    void setState(double value) {
        state = std::max(0.0, std::min(100.0, value));
        active = state > 0;
    }

    double getState() const { return state; }
    bool isActive() const { return active; }
    std::string getName() const { return name; }
};

// =============================================================================
// SECTION 8 : SYSTÈME DE NAVIGATION ROBOTIQUE
// =============================================================================

class RobotNavigationSystem {
private:
    std::shared_ptr<QuantumClassicalBridge> bridge;
    std::shared_ptr<LogicProcessor> logic;
    SystemMode mode;
    
    std::map<std::string, std::unique_ptr<SensorSimulator>> sensors;
    std::map<std::string, std::unique_ptr<ActuatorSimulator>> actuators;
    
    double obstacle_threshold;
    std::vector<NavigationDecision> navigation_log;

public:
    RobotNavigationSystem(std::shared_ptr<QuantumClassicalBridge> b,
                          std::shared_ptr<LogicProcessor> l)
        : bridge(b), logic(l), mode(SystemMode::AUTONOMOUS), obstacle_threshold(40.0) {
        
        // Initialisation des capteurs
        sensors["front"] = std::make_unique<SensorSimulator>("front_distance");
        sensors["left"] = std::make_unique<SensorSimulator>("left_distance");
        sensors["right"] = std::make_unique<SensorSimulator>("right_distance");
        
        // Initialisation des actionneurs
        actuators["left_motor"] = std::make_unique<ActuatorSimulator>("left_motor");
        actuators["right_motor"] = std::make_unique<ActuatorSimulator>("right_motor");
        actuators["servo"] = std::make_unique<ActuatorSimulator>("servo");
    }

    std::map<std::string, double> readAllSensors() {
        std::map<std::string, double> readings;
        for (auto& [name, sensor] : sensors) {
            readings[name] = sensor->read();
        }
        return readings;
    }

    NavigationDecision evaluatePath(const std::map<std::string, double>& readings) {
        bool front_clear = readings.at("front") >= obstacle_threshold;
        bool left_clear = readings.at("left") >= obstacle_threshold;
        bool right_clear = readings.at("right") >= obstacle_threshold;

        // Évaluation avec logique AND/XOR
        logic->execute(OperationType::AND, {front_clear, left_clear, right_clear},
                      "Full path evaluation");

        NavigationDecision decision;
        
        if (front_clear) {
            decision = NavigationDecision::FORWARD;
        } else {
            logic->execute(OperationType::XOR, {left_clear, right_clear},
                          "Direction decision");
            
            if (left_clear && !right_clear) {
                decision = NavigationDecision::TURN_LEFT;
            } else if (right_clear && !left_clear) {
                decision = NavigationDecision::TURN_RIGHT;
            } else if (left_clear && right_clear) {
                decision = (readings.at("left") > readings.at("right")) 
                          ? NavigationDecision::TURN_LEFT 
                          : NavigationDecision::TURN_RIGHT;
            } else {
                decision = NavigationDecision::REVERSE;
            }
        }

        navigation_log.push_back(decision);
        return decision;
    }

    void executeMovement(NavigationDecision decision) {
        static const std::map<NavigationDecision, std::pair<double, double>> movements = {
            {NavigationDecision::FORWARD, {80, 80}},
            {NavigationDecision::TURN_LEFT, {40, 80}},
            {NavigationDecision::TURN_RIGHT, {80, 40}},
            {NavigationDecision::REVERSE, {60, 60}},
            {NavigationDecision::STOP, {0, 0}}
        };

        auto it = movements.find(decision);
        if (it != movements.end()) {
            actuators["left_motor"]->setState(it->second.first);
            actuators["right_motor"]->setState(it->second.second);
        }

        static const std::map<NavigationDecision, std::string> names = {
            {NavigationDecision::FORWARD, "FORWARD"},
            {NavigationDecision::TURN_LEFT, "TURN_LEFT"},
            {NavigationDecision::TURN_RIGHT, "TURN_RIGHT"},
            {NavigationDecision::REVERSE, "REVERSE"},
            {NavigationDecision::STOP, "STOP"}
        };

        std::cout << "[NAVIGATION] Executing: " << names.at(decision) << std::endl;
    }

    void runCycle() {
        auto readings = readAllSensors();
        
        std::cout << "\n[SENSORS] F:" << std::fixed << std::setprecision(1)
                  << readings["front"] << " L:" << readings["left"] 
                  << " R:" << readings["right"] << std::endl;
        
        NavigationDecision decision = evaluatePath(readings);
        executeMovement(decision);
    }

    size_t getNavigationLogSize() const { return navigation_log.size(); }
};

// =============================================================================
// SECTION 9 : GESTIONNAIRE DE RÉSILIENCE
// =============================================================================

class ResilienceManager {
private:
    int error_count;
    int recovery_count;

public:
    ResilienceManager() : error_count(0), recovery_count(0) {}

    template<typename Func, typename Fallback>
    auto executeWithResilience(Func operation, Fallback fallback, 
                               int max_retries = 3) -> decltype(fallback) {
        for (int attempt = 0; attempt < max_retries; attempt++) {
            try {
                return operation();
            } catch (const std::exception& e) {
                error_count++;
                std::cout << "[RESILIENCE] Attempt " << (attempt + 1) 
                          << " failed: " << e.what() << std::endl;
                std::this_thread::sleep_for(std::chrono::milliseconds(100 * (attempt + 1)));
            }
        }
        
        recovery_count++;
        std::cout << "[RESILIENCE] Using fallback value" << std::endl;
        return fallback;
    }

    int getErrorCount() const { return error_count; }
    int getRecoveryCount() const { return recovery_count; }
};

// =============================================================================
// SECTION 10 : SYSTÈME UNIFIÉ
// =============================================================================

class UnifiedRobotSystem {
private:
    std::shared_ptr<VisualizationEngine> viz;
    std::shared_ptr<QuantumClassicalBridge> bridge;
    std::shared_ptr<LogicProcessor> logic;
    std::unique_ptr<RobotNavigationSystem> navigation;
    std::unique_ptr<ResilienceManager> resilience;

public:
    UnifiedRobotSystem(int animation_delay = 150) {
        std::cout << "\n" << std::string(70, '=') << std::endl;
        std::cout << "UNIFIED ROBOT SYSTEM - INITIALIZATION" << std::endl;
        std::cout << std::string(70, '=') << std::endl;

        viz = std::make_shared<VisualizationEngine>(animation_delay);
        bridge = std::make_shared<QuantumClassicalBridge>(viz);
        logic = std::make_shared<LogicProcessor>(bridge, viz);
        navigation = std::make_unique<RobotNavigationSystem>(bridge, logic);
        resilience = std::make_unique<ResilienceManager>();

        bridge->describeParadigm();
        
        std::cout << "[SYSTEM] All components initialized" << std::endl;
        std::cout << std::string(70, '=') << "\n" << std::endl;
    }

    void runLogicTests() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "LOGIC OPERATIONS TEST" << std::endl;
        std::cout << std::string(50, '=') << std::endl;

        logic->execute(OperationType::AND, {true, true}, "AND(1,1)");
        logic->execute(OperationType::AND, {true, false}, "AND(1,0)");
        logic->execute(OperationType::XOR, {true, true}, "XOR(1,1)");
        logic->execute(OperationType::XOR, {true, false}, "XOR(1,0)");
        logic->execute(OperationType::OR, {false, false, true}, "OR(0,0,1)");
        logic->execute(OperationType::NOT, {true}, "NOT(1)");
    }

    void runNavigationSimulation(int cycles = 3) {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "ROBOT NAVIGATION SIMULATION" << std::endl;
        std::cout << std::string(50, '=') << std::endl;

        for (int i = 0; i < cycles; i++) {
            std::cout << "\n--- Cycle " << (i + 1) << "/" << cycles << " ---" << std::endl;
            navigation->runCycle();
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }

    void runResilienceTest() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "RESILIENCE TEST" << std::endl;
        std::cout << std::string(50, '=') << std::endl;

        // Test réussi
        auto success = resilience->executeWithResilience(
            []() { return std::string("Success!"); },
            std::string("Fallback")
        );
        std::cout << "Success test result: " << success << std::endl;

        // Test échoué
        int fail_counter = 0