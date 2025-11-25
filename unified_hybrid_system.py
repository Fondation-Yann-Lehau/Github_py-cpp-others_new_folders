"""
Système Hybride Unifié
======================
Architecture technique combinant :
- Logique binaire classique (AND/XOR/NOT)
- Transitions quantique-symbolique
- Traitement de données avec transformation exponentielle
- Analyse et catégorisation d'entités
- Évaluation de sécurité paramétrable
- Quantification de facteurs abstraits
- Gestion d'exceptions et résilience
"""

import math
import sys
import time
import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from abc import ABC, abstractmethod


# =============================================================================
# SECTION 1 : ÉNUMÉRATIONS ET STRUCTURES DE DONNÉES
# =============================================================================

class BinaryState(Enum):
    """États binaires classiques avec sémantique enrichie."""
    ZERO = 0  # Conjonction/Intégration/Annulation
    ONE = 1   # Initiation/Structuration/Activation


class OperationType(Enum):
    """Types d'opérations logiques supportées."""
    AND = auto()      # Conjonction
    OR = auto()       # Disjonction
    XOR = auto()      # Exclusion/Annulation
    NOT = auto()      # Négation
    NAND = auto()     # Non-ET
    NOR = auto()      # Non-OU


class SystemMode(Enum):
    """Modes de fonctionnement du système."""
    AUTONOMOUS = auto()
    MANUAL = auto()
    HYBRID = auto()


@dataclass
class QuantumState:
    """Représentation d'un état quantique symbolique."""
    alpha: float = 0.707  # Amplitude de |1⟩
    beta: float = 0.707   # Amplitude de |0⟩
    
    def __post_init__(self):
        # Normalisation automatique
        norm = math.sqrt(self.alpha**2 + self.beta**2)
        if norm > 0:
            self.alpha /= norm
            self.beta /= norm
    
    @property
    def probability_one(self) -> float:
        return self.alpha ** 2
    
    @property
    def probability_zero(self) -> float:
        return self.beta ** 2
    
    def collapse(self) -> BinaryState:
        """Effondrement de la fonction d'onde."""
        import random
        return BinaryState.ONE if random.random() < self.probability_one else BinaryState.ZERO


@dataclass
class ProcessingResult:
    """Résultat d'une opération de traitement."""
    success: bool
    value: Any
    context: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# SECTION 2 : INTERFACE DE VISUALISATION
# =============================================================================

class VisualizationEngine:
    """Moteur de visualisation ASCII pour les transitions et processus."""
    
    def __init__(self, animation_delay: float = 0.15):
        self.delay = animation_delay
        self.enabled = True
    
    def _write_flush(self, text: str):
        if self.enabled:
            sys.stdout.write(text)
            sys.stdout.flush()
    
    def visualize_wave_collapse(self, final_state: BinaryState) -> None:
        """Visualisation de l'effondrement onde → particule."""
        if not self.enabled:
            return
            
        stages = [
            ("~ ~ ~", "WAVE"),
            ("(•)", "TRANSITION"),
        ]
        
        self._write_flush(" | Processing: ")
        
        for symbol, label in stages:
            self._write_flush(f"{symbol} ({label}) ")
            time.sleep(self.delay)
            self._write_flush("→ ")
            time.sleep(self.delay)
        
        if final_state == BinaryState.ONE:
            print("[ 1 ] (CRYSTALLIZED)")
        else:
            print("[ 0 ] (ANNULLED)")
        print("-" * 50)
    
    def visualize_data_flow(self, data_points: List[float], label: str = "Data") -> None:
        """Visualisation du flux de données."""
        if not self.enabled or not data_points:
            return
            
        max_val = max(data_points) if data_points else 1
        normalized = [int((v / max_val) * 20) for v in data_points[:10]]
        
        print(f"\n[{label}] Flow Visualization:")
        for i, height in enumerate(normalized):
            bar = "█" * height + "░" * (20 - height)
            print(f"  [{i:02d}] {bar} {data_points[i]:.2e}")
    
    def visualize_operation(self, op_type: OperationType, inputs: Tuple, output: bool) -> None:
        """Visualisation d'une opération logique."""
        symbols = {
            OperationType.AND: "∧",
            OperationType.OR: "∨",
            OperationType.XOR: "⊕",
            OperationType.NOT: "¬",
            OperationType.NAND: "⊼",
            OperationType.NOR: "⊽",
        }
        symbol = symbols.get(op_type, "?")
        inputs_str = f" {symbol} ".join(str(int(i)) for i in inputs)
        print(f"  Operation: {inputs_str} = {int(output)}")


# =============================================================================
# SECTION 3 : MOTEUR DE TRANSITION QUANTIQUE-CLASSIQUE
# =============================================================================

class QuantumClassicalBridge:
    """
    Pont entre logique quantique symbolique et exécution classique.
    Gère la transition du potentiel (onde) vers le déterministe (particule).
    """
    
    def __init__(self, visualization: Optional[VisualizationEngine] = None):
        self.viz = visualization or VisualizationEngine()
        self._transition_count = 0
        self._history: List[ProcessingResult] = []
    
    def describe_paradigm(self) -> None:
        """Décrit le paradigme de transition."""
        print("\n" + "=" * 60)
        print("QUANTUM-CLASSICAL BRIDGE INITIALIZED")
        print("=" * 60)
        print("Paradigm: Binary states as cycloidal transitions")
        print("  - State |1⟩: Initiation/Structuration")
        print("  - State |0⟩: Integration/Completion")
        print("  - Superposition: Potential before observation")
        print("=" * 60 + "\n")
    
    def interpret_state(
        self, 
        potential_state: bool, 
        context: str,
        visualize: bool = True
    ) -> ProcessingResult:
        """
        Force l'effondrement du potentiel en état classique.
        
        Args:
            potential_state: État potentiel calculé
            context: Contexte de l'observation
            visualize: Activer la visualisation
            
        Returns:
            ProcessingResult avec l'état fixé
        """
        self._transition_count += 1
        
        print(f"\n[OBSERVATION #{self._transition_count}] Context: {context}")
        
        final_state = BinaryState.ONE if potential_state else BinaryState.ZERO
        
        if visualize:
            self.viz.visualize_wave_collapse(final_state)
        
        result = ProcessingResult(
            success=True,
            value=final_state,
            context=context,
            metadata={"transition_id": self._transition_count}
        )
        self._history.append(result)
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques des transitions."""
        if not self._history:
            return {"total": 0, "ones": 0, "zeros": 0}
        
        ones = sum(1 for r in self._history if r.value == BinaryState.ONE)
        return {
            "total": len(self._history),
            "ones": ones,
            "zeros": len(self._history) - ones,
            "ratio_one": ones / len(self._history)
        }


# =============================================================================
# SECTION 4 : PROCESSEUR DE TRANSFORMATION DE DONNÉES
# =============================================================================

class DataTransformationProcessor:
    """
    Processeur de transformation de données.
    Applique des transformations exponentielles et autres sur des données brutes.
    """
    
    def __init__(self, overflow_threshold: float = 700.0):
        self.overflow_threshold = overflow_threshold
        self._processed_count = 0
    
    def transform_exponential(self, data: str) -> ProcessingResult:
        """
        Applique une transformation exponentielle sur la représentation en octets.
        
        Args:
            data: Chaîne de caractères à transformer
            
        Returns:
            ProcessingResult contenant les valeurs transformées
        """
        try:
            byte_array = bytearray(data, 'utf-8')
            transformed = []
            
            for byte in byte_array:
                if byte > self.overflow_threshold:
                    # Utiliser log-scale pour éviter overflow
                    transformed.append(math.log1p(math.exp(self.overflow_threshold)) + byte)
                else:
                    transformed.append(math.exp(byte))
            
            self._processed_count += 1
            
            return ProcessingResult(
                success=True,
                value=transformed,
                context="Exponential transformation",
                metadata={
                    "input_length": len(data),
                    "output_length": len(transformed),
                    "min_value": min(transformed) if transformed else 0,
                    "max_value": max(transformed) if transformed else 0
                }
            )
            
        except Exception as e:
            return ProcessingResult(
                success=False,
                value=None,
                context=f"Transformation error: {str(e)}"
            )
    
    def transform_normalized(self, data: str) -> ProcessingResult:
        """Transformation avec normalisation [0, 1]."""
        exp_result = self.transform_exponential(data)
        
        if not exp_result.success:
            return exp_result
        
        values = exp_result.value
        min_v, max_v = min(values), max(values)
        range_v = max_v - min_v if max_v != min_v else 1
        
        normalized = [(v - min_v) / range_v for v in values]
        
        return ProcessingResult(
            success=True,
            value=normalized,
            context="Normalized transformation",
            metadata={"original_range": (min_v, max_v)}
        )
    
    def compute_hash_signature(self, data: str) -> ProcessingResult:
        """Calcule une signature numérique basée sur les transformations."""
        exp_result = self.transform_exponential(data)
        
        if not exp_result.success:
            return exp_result
        
        values = exp_result.value
        signature = sum(v * (i + 1) for i, v in enumerate(values)) % (2**32)
        
        return ProcessingResult(
            success=True,
            value=signature,
            context="Hash signature computation",
            metadata={"algorithm": "weighted_sum_mod32"}
        )


# =============================================================================
# SECTION 5 : ANALYSEUR D'ENTITÉS ET CATÉGORISATEUR
# =============================================================================

class EntityAnalyzer:
    """
    Analyseur et catégorisateur d'entités textuelles.
    Utilise le pattern matching pour identifier et classer les éléments.
    """
    
    def __init__(self):
        self.categories: Dict[str, List[str]] = defaultdict(list)
        self.patterns: Dict[str, List[str]] = {
            "TECHNICAL": ["http", "https", "www", ".com", ".org", ".fr", ".eu"],
            "COMMUNICATION": ["@", "mail", "contact", "info"],
            "NUMERIC": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
            "PROTOCOL": ["ftp", "ssh", "tcp", "udp", "api"],
        }
        self._analysis_count = 0
    
    def add_custom_pattern(self, category: str, patterns: List[str]) -> None:
        """Ajoute des patterns personnalisés pour une catégorie."""
        if category not in self.patterns:
            self.patterns[category] = []
        self.patterns[category].extend(patterns)
    
    def analyze(self, content: str) -> ProcessingResult:
        """
        Analyse et catégorise le contenu textuel.
        
        Args:
            content: Texte à analyser
            
        Returns:
            ProcessingResult avec les catégories identifiées
        """
        self._analysis_count += 1
        content_lower = content.lower()
        matches: Dict[str, int] = defaultdict(int)
        
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if pattern.lower() in content_lower:
                    matches[category] += content_lower.count(pattern.lower())
                    if content not in self.categories[category]:
                        self.categories[category].append(content[:100])
        
        primary_category = max(matches, key=matches.get) if matches else "UNKNOWN"
        
        return ProcessingResult(
            success=True,
            value={
                "primary_category": primary_category,
                "all_matches": dict(matches),
                "confidence": matches[primary_category] / sum(matches.values()) if matches else 0
            },
            context="Entity categorization",
            metadata={"content_preview": content[:50]}
        )
    
    def get_category_summary(self) -> Dict[str, int]:
        """Retourne un résumé des catégories identifiées."""
        return {cat: len(items) for cat, items in self.categories.items()}


# =============================================================================
# SECTION 6 : ÉVALUATEUR DE SÉCURITÉ
# =============================================================================

class SecurityEvaluator:
    """
    Évaluateur de niveaux de sécurité avec scoring paramétrable.
    """
    
    def __init__(self, base_coefficient: float = 0.873):
        self.coefficient = base_coefficient
        self.rules: Dict[str, float] = {
            "professional_network": 9.2,
            "social_network": 7.4,
            "government": 8.5,
            "educational": 8.0,
            "commercial": 6.0,
            "default": 5.0
        }
        self._evaluations: List[ProcessingResult] = []
    
    def add_rule(self, category: str, base_score: float) -> None:
        """Ajoute une règle de scoring."""
        self.rules[category] = base_score
    
    def evaluate(self, identifier: str) -> ProcessingResult:
        """
        Évalue le niveau de sécurité d'un identifiant.
        
        Args:
            identifier: Identifiant à évaluer
            
        Returns:
            ProcessingResult avec le score de sécurité
        """
        identifier_lower = identifier.lower()
        
        # Détermination de la catégorie
        category = "default"
        if any(x in identifier_lower for x in ["linkedin", "professional"]):
            category = "professional_network"
        elif any(x in identifier_lower for x in ["facebook", "twitter", "instagram"]):
            category = "social_network"
        elif any(x in identifier_lower for x in [".gov", ".gouv", "government"]):
            category = "government"
        elif any(x in identifier_lower for x in [".edu", "university", "school"]):
            category = "educational"
        elif any(x in identifier_lower for x in [".com", "shop", "store"]):
            category = "commercial"
        
        base_score = self.rules.get(category, self.rules["default"])
        final_score = base_score * self.coefficient
        
        result = ProcessingResult(
            success=True,
            value={
                "score": final_score,
                "max_score": 10.0,
                "category": category,
                "normalized": final_score / 10.0
            },
            context="Security evaluation",
            metadata={"identifier_hash": hash(identifier) % 10000}
        )
        self._evaluations.append(result)
        
        return result
    
    def get_evaluation_statistics(self) -> Dict[str, Any]:
        """Retourne les statistiques des évaluations."""
        if not self._evaluations:
            return {"count": 0}
        
        scores = [e.value["score"] for e in self._evaluations]
        return {
            "count": len(scores),
            "mean": sum(scores) / len(scores),
            "min": min(scores),
            "max": max(scores)
        }


# =============================================================================
# SECTION 7 : QUANTIFICATEUR DE FACTEURS ABSTRAITS
# =============================================================================

class AbstractFactorQuantifier:
    """
    Quantificateur de facteurs abstraits avec mapping configurable.
    Transforme des concepts abstraits en valeurs numériques pondérées.
    """
    
    def __init__(self, coefficient: float = 1.0):
        self.coefficient = coefficient
        self.factor_map: Dict[str, float] = {
            "stability": 2.342e-8,
            "entropy": 9.412e-5,
            "harmony": 3.1415926535,
            "complexity": 11.0901,
            "coherence": 1.61803398875,  # Golden ratio
            "resonance": 2.71828182845,  # Euler's number
        }
        self.signatures: List[Dict[str, float]] = []
    
    def add_factor(self, name: str, base_value: float) -> None:
        """Ajoute un facteur personnalisé."""
        self.factor_map[name.lower()] = base_value
    
    def quantify(self, factors: Optional[List[str]] = None) -> ProcessingResult:
        """
        Quantifie les facteurs spécifiés ou tous les facteurs.
        
        Args:
            factors: Liste des facteurs à quantifier (None = tous)
            
        Returns:
            ProcessingResult avec les valeurs quantifiées
        """
        target_factors = factors or list(self.factor_map.keys())
        
        quantified = {}
        for factor in target_factors:
            factor_lower = factor.lower()
            if factor_lower in self.factor_map:
                quantified[factor_lower] = self.factor_map[factor_lower] * self.coefficient
        
        if quantified:
            self.signatures.append(quantified)
        
        return ProcessingResult(
            success=bool(quantified),
            value=quantified,
            context="Abstract factor quantification",
            metadata={
                "factors_requested": len(target_factors),
                "factors_found": len(quantified)
            }
        )
    
    def compute_composite_score(self) -> float:
        """Calcule un score composite de toutes les signatures."""
        if not self.signatures:
            return 0.0
        
        total = sum(sum(sig.values()) for sig in self.signatures)
        return total / len(self.signatures)


# =============================================================================
# SECTION 8 : GESTIONNAIRE DE CHEMINS SYSTÈME
# =============================================================================

class SystemPathManager:
    """
    Gestionnaire dynamique de chemins système.
    Permet l'ajout et la gestion sécurisée de chemins de modules.
    """
    
    def __init__(self):
        self.added_paths: List[str] = []
        self.original_path_count = len(sys.path)
    
    def add_path(self, path: str) -> ProcessingResult:
        """
        Ajoute un chemin au système si non existant.
        
        Args:
            path: Chemin à ajouter
            
        Returns:
            ProcessingResult indiquant le succès de l'opération
        """
        if path in sys.path:
            return ProcessingResult(
                success=True,
                value=False,
                context=f"Path already exists: {path}",
                metadata={"action": "skipped"}
            )
        
        sys.path.append(path)
        self.added_paths.append(path)
        
        return ProcessingResult(
            success=True,
            value=True,
            context=f"Path added: {path}",
            metadata={"action": "added", "total_paths": len(sys.path)}
        )
    
    def remove_added_paths(self) -> int:
        """Supprime tous les chemins ajoutés par ce gestionnaire."""
        removed = 0
        for path in self.added_paths:
            if path in sys.path:
                sys.path.remove(path)
                removed += 1
        self.added_paths.clear()
        return removed
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut du gestionnaire."""
        return {
            "original_count": self.original_path_count,
            "current_count": len(sys.path),
            "added_by_manager": len(self.added_paths)
        }


# =============================================================================
# SECTION 9 : PROCESSEUR D'OPÉRATIONS LOGIQUES
# =============================================================================

class LogicOperationProcessor:
    """
    Processeur d'opérations logiques binaires avec support étendu.
    """
    
    def __init__(self, quantum_bridge: Optional[QuantumClassicalBridge] = None):
        self.bridge = quantum_bridge or QuantumClassicalBridge()
        self.viz = self.bridge.viz
        self._operation_log: List[Tuple[OperationType, Tuple, bool]] = []
    
    def execute(
        self, 
        op_type: OperationType, 
        *inputs: bool,
        context: str = "",
        use_quantum: bool = True
    ) -> ProcessingResult:
        """
        Exécute une opération logique.
        
        Args:
            op_type: Type d'opération
            inputs: Entrées booléennes
            context: Contexte de l'opération
            use_quantum: Utiliser le pont quantique
            
        Returns:
            ProcessingResult avec le résultat de l'opération
        """
        if len(inputs) < 1:
            return ProcessingResult(False, None, "No inputs provided")
        
        # Calcul du résultat brut
        if op_type == OperationType.AND:
            raw_result = all(inputs)
        elif op_type == OperationType.OR:
            raw_result = any(inputs)
        elif op_type == OperationType.XOR:
            raw_result = sum(inputs) % 2 == 1
        elif op_type == OperationType.NOT:
            raw_result = not inputs[0]
        elif op_type == OperationType.NAND:
            raw_result = not all(inputs)
        elif op_type == OperationType.NOR:
            raw_result = not any(inputs)
        else:
            return ProcessingResult(False, None, f"Unknown operation: {op_type}")
        
        # Enregistrement
        self._operation_log.append((op_type, inputs, raw_result))
        
        # Visualisation
        self.viz.visualize_operation(op_type, inputs, raw_result)
        
        # Interprétation via pont quantique si demandé
        if use_quantum:
            full_context = f"{op_type.name}: {context}" if context else op_type.name
            quantum_result = self.bridge.interpret_state(raw_result, full_context)
            return quantum_result
        
        return ProcessingResult(
            success=True,
            value=BinaryState.ONE if raw_result else BinaryState.ZERO,
            context=f"{op_type.name} operation"
        )
    
    def get_operation_statistics(self) -> Dict[str, int]:
        """Retourne les statistiques des opérations effectuées."""
        stats = defaultdict(int)
        for op_type, _, _ in self._operation_log:
            stats[op_type.name] += 1
        return dict(stats)


# =============================================================================
# SECTION 10 : GESTIONNAIRE D'EXCEPTIONS ET RÉSILIENCE
# =============================================================================

class ResilienceManager:
    """
    Gestionnaire de résilience et de récupération après erreurs.
    Implémente des stratégies de fallback et de restauration.
    """
    
    def __init__(self):
        self.error_log: List[Dict[str, Any]] = []
        self.recovery_count = 0
        self.checkpoint_data: Dict[str, Any] = {}
    
    def create_checkpoint(self, name: str, data: Any) -> None:
        """Crée un point de sauvegarde."""
        self.checkpoint_data[name] = {
            "data": data,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def restore_checkpoint(self, name: str) -> Optional[Any]:
        """Restaure un point de sauvegarde."""
        if name in self.checkpoint_data:
            self.recovery_count += 1
            return self.checkpoint_data[name]["data"]
        return None
    
    def execute_with_resilience(
        self, 
        operation: callable,
        fallback_value: Any = None,
        max_retries: int = 3,
        context: str = ""
    ) -> ProcessingResult:
        """
        Exécute une opération avec gestion de résilience.
        
        Args:
            operation: Fonction à exécuter
            fallback_value: Valeur de secours
            max_retries: Nombre maximum de tentatives
            context: Contexte de l'opération
            
        Returns:
            ProcessingResult avec le résultat ou la valeur de secours
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result = operation()
                return ProcessingResult(
                    success=True,
                    value=result,
                    context=context,
                    metadata={"attempts": attempt + 1}
                )
            except Exception as e:
                last_error = e
                self.error_log.append({
                    "context": context,
                    "attempt": attempt + 1,
                    "error": str(e),
                    "timestamp": datetime.datetime.now().isoformat()
                })
                time.sleep(0.1 * (attempt + 1))  # Backoff exponentiel simplifié
        
        # Fallback
        self.recovery_count += 1
        return ProcessingResult(
            success=False,
            value=fallback_value,
            context=f"{context} - FALLBACK USED",
            metadata={
                "error": str(last_error),
                "attempts": max_retries
            }
        )
    
    def get_health_report(self) -> Dict[str, Any]:
        """Retourne un rapport de santé du système."""
        return {
            "total_errors": len(self.error_log),
            "recoveries": self.recovery_count,
            "checkpoints": len(self.checkpoint_data),
            "recent_errors": self.error_log[-5:] if self.error_log else []
        }


# =============================================================================
# SECTION 11 : SIMULATEUR ROBOTIQUE GÉNÉRIQUE
# =============================================================================

class GenericSensorSimulator:
    """Simulateur de capteur générique."""
    
    def __init__(self, name: str, min_val: float = 0, max_val: float = 400):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
    
    def read(self) -> float:
        """Simule une lecture de capteur."""
        import random
        return random.uniform(self.min_val, self.max_val)


class GenericActuatorSimulator:
    """Simulateur d'actionneur générique."""
    
    def __init__(self, name: str):
        self.name = name
        self.state = 0.0
        self.active = False
    
    def set_state(self, value: float) -> None:
        """Définit l'état de l'actionneur."""
        self.state = max(0, min(100, value))
        self.active = self.state > 0
    
    def get_state(self) -> Dict[str, Any]:
        return {"name": self.name, "state": self.state, "active": self.active}


class RobotNavigationSystem:
    """
    Système de navigation robotique générique.
    Implémente une architecture comportementale/hybride.
    """
    
    def __init__(
        self, 
        quantum_bridge: QuantumClassicalBridge,
        logic_processor: LogicOperationProcessor
    ):
        self.bridge = quantum_bridge
        self.logic = logic_processor
        self.mode = SystemMode.AUTONOMOUS
        
        # Capteurs simulés
        self.sensors = {
            "front": GenericSensorSimulator("front_distance"),
            "left": GenericSensorSimulator("left_distance"),
            "right": GenericSensorSimulator("right_distance"),
        }
        
        # Actionneurs simulés
        self.actuators = {
            "left_motor": GenericActuatorSimulator("left_motor"),
            "right_motor": GenericActuatorSimulator("right_motor"),
            "servo": GenericActuatorSimulator("servo"),
        }
        
        self.obstacle_threshold = 40.0
        self._navigation_log: List[str] = []
    
    def read_all_sensors(self) -> Dict[str, float]:
        """Lit tous les capteurs."""
        return {name: sensor.read() for name, sensor in self.sensors.items()}
    
    def evaluate_path(self, readings: Dict[str, float]) -> ProcessingResult:
        """
        Évalue le chemin basé sur les lectures de capteurs.
        Utilise la logique AND/XOR pour la décision.
        """
        front_clear = readings["front"] >= self.obstacle_threshold
        left_clear = readings["left"] >= self.obstacle_threshold
        right_clear = readings["right"] >= self.obstacle_threshold
        
        # Conjonction : chemin complètement dégagé
        all_clear_result = self.logic.execute(
            OperationType.AND,
            front_clear, left_clear, right_clear,
            context="Full path evaluation"
        )
        
        # Décision de direction si obstacle frontal
        if not front_clear:
            # XOR pour choisir entre gauche et droite
            direction_result = self.logic.execute(
                OperationType.XOR,
                left_clear, right_clear,
                context="Direction decision"
            )
            
            if left_clear and not right_clear:
                decision = "TURN_LEFT"
            elif right_clear and not left_clear:
                decision = "TURN_RIGHT"
            elif left_clear and right_clear:
                decision = "TURN_LEFT" if readings["left"] > readings["right"] else "TURN_RIGHT"
            else:
                decision = "REVERSE"
        else:
            decision = "FORWARD"
        
        self._navigation_log.append(decision)
        
        return ProcessingResult(
            success=True,
            value=decision,
            context="Navigation decision",
            metadata={"readings": readings, "all_clear": all_clear_result.value}
        )
    
    def execute_movement(self, decision: str) -> None:
        """Exécute un mouvement basé sur la décision."""
        movements = {
            "FORWARD": (80, 80),
            "TURN_LEFT": (40, 80),
            "TURN_RIGHT": (80, 40),
            "REVERSE": (-60, -60),
            "STOP": (0, 0),
        }
        
        left_speed, right_speed = movements.get(decision, (0, 0))
        self.actuators["left_motor"].set_state(abs(left_speed))
        self.actuators["right_motor"].set_state(abs(right_speed))
        
        print(f"[NAVIGATION] Executing: {decision} (L:{left_speed}, R:{right_speed})")
    
    def run_cycle(self) -> ProcessingResult:
        """Exécute un cycle complet de navigation."""
        readings = self.read_all_sensors()
        print(f"\n[SENSORS] F:{readings['front']:.1f} L:{readings['left']:.1f} R:{readings['right']:.1f}")
        
        decision_result = self.evaluate_path(readings)
        self.execute_movement(decision_result.value)
        
        return decision_result


# =============================================================================
# SECTION 12 : SYSTÈME UNIFIÉ COMPLET
# =============================================================================

class UnifiedHybridSystem:
    """
    Système unifié intégrant toutes les composantes.
    Point d'entrée principal pour l'utilisation du framework.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        
        print("\n" + "=" * 70)
        print("UNIFIED HYBRID SYSTEM - INITIALIZATION")
        print("=" * 70)
        
        # Initialisation des composants
        self.viz = VisualizationEngine(
            animation_delay=config.get("animation_delay", 0.15)
        )
        self.viz.enabled = config.get("visualization_enabled", True)
        
        self.quantum_bridge = QuantumClassicalBridge(self.viz)
        self.quantum_bridge.describe_paradigm()
        
        self.data_processor = DataTransformationProcessor()
        self.entity_analyzer = EntityAnalyzer()
        self.security_evaluator = SecurityEvaluator(
            base_coefficient=config.get("security_coefficient", 0.873)
        )
        self.factor_quantifier = AbstractFactorQuantifier(
            coefficient=config.get("quantification_coefficient", 1.0)
        )
        self.path_manager = SystemPathManager()
        self.logic_processor = LogicOperationProcessor(self.quantum_bridge)
        self.resilience = ResilienceManager()
        
        self.robot_nav = RobotNavigationSystem(
            self.quantum_bridge,
            self.logic_processor
        )
        
        self._initialized_at = datetime.datetime.now().isoformat()
        print(f"\n[SYSTEM] All components initialized at {self._initialized_at}")
        print("=" * 70 + "\n")
    
    def process_data_sample(self, data: str) -> Dict[str, ProcessingResult]:
        """Traite un échantillon de données à travers tous les processeurs."""
        results = {}
        
        # Transformation exponentielle
        results["transformation"] = self.data_processor.transform_exponential(data)
        
        # Analyse d'entités
        results["entity_analysis"] = self.entity_analyzer.analyze(data)
        
        # Évaluation de sécurité
        results["security"] = self.security_evaluator.evaluate(data)
        
        return results
    
    def execute_logic_sequence(
        self, 
        operations: List[Tuple[OperationType, Tuple[bool, ...]]]
    ) -> List[ProcessingResult]:
        """Exécute une séquence d'opérations logiques."""
        results = []
        for op_type, inputs in operations:
            result = self.logic_processor.execute(op_type, *inputs)
            results.append(result)
        return results
    
    def run_robot_simulation(self, cycles: int = 5) -> List[ProcessingResult]:
        """Exécute une simulation de navigation robotique."""
        print("\n" + "=" * 50)
        print("ROBOT NAVIGATION SIMULATION")
        print("=" * 50)
        
        results = []
        for i in range(cycles):
            print(f"\n--- Cycle {i + 1}/{cycles} ---")
            result = self.robot_nav.run_cycle()
            results.append(result)
            time.sleep(0.5)
        
        return results
    
    def get_system_report(self) -> Dict[str, Any]:
        """Génère un rapport complet du système."""
        return {
            "initialization_time": self._initialized_at,
            "quantum_statistics": self.quantum_bridge.get_statistics(),
            "entity_categories": self.entity_analyzer.get_category_summary(),
            "security_statistics": self.security_evaluator.get_evaluation_statistics(),
            "logic_operations": self.logic_processor.get_operation_statistics(),
            "resilience_health": self.resilience.get_health_report(),
            "path_manager_status": self.path_manager.get_status(),
            "factor_composite_score": self.factor_quantifier.compute_composite_score()
        }


# =============================================================================
# SECTION 13 : DÉMONSTRATION ET TESTS
# =============================================================================

def run_demonstration():
    """Fonction de démonstration complète du système."""
    
    print("\n" + "#" * 70)
    print("#" + " " * 20 + "SYSTEM DEMONSTRATION" + " " * 20 + "#")
    print("#" * 70 + "\n")
    
    # Configuration
    config = {
        "animation_delay": 0.1,
        "visualization_enabled": True,
        "security_coefficient": 0.873,
        "quantification_coefficient": 1.0
    }
    
    # Initialisation du système
    system = UnifiedHybridSystem(config)
    
    # --- Test 1: Opérations Logiques ---
    print("\n" + "=" * 50)
    print("TEST 1: LOGIC OPERATIONS")
    print("=" * 50)
    
    operations = [
        (OperationType.AND, (True, True)),
        (OperationType.AND, (True, False)),
        (OperationType.XOR, (True, True)),
        (OperationType.XOR, (True, False)),
        (OperationType.OR, (False, False, True)),
        (OperationType.NOT, (True,)),
    ]
    
    logic_results = system.execute_logic_sequence(operations)
    
    # --- Test 2: Transformation de Données ---
    print("\n" + "=" * 50)
    print("TEST 2: DATA TRANSFORMATION")
    print("=" * 50)
    
    test_data = "Sample data for transformation testing 12345"
    transform_result = system.data_processor.transform_exponential(test_data)
    
    if transform_result.success:
        print(f"Input length: {len(test_data)}")
        print(f"Output length: {len(transform_result.value)}")
        print(f"First 5 values: {transform_result.value[:5]}")
        system.viz.visualize_data_flow(transform_result.value[:20], "Exponential Transform")
    
    # --- Test 3: Quantification de Facteurs ---
    print("\n" + "=" * 50)
    print("TEST 3: ABSTRACT FACTOR QUANTIFICATION")
    print("=" * 50)
    
    factors = ["stability", "entropy", "harmony", "complexity"]
    quant_result = system.factor_quantifier.quantify(factors)
    
    if quant_result.success:
        for factor, value in quant_result.value.items():
            print(f"  {factor}: {value:.6e}")
    
    # --- Test 4: Simulation Robotique ---
    print("\n" + "=" * 50)
    print("TEST 4: ROBOT NAVIGATION SIMULATION")
    print("=" * 50)
    
    nav_results = system.run_robot_simulation(cycles=3)
    
    # --- Test 5: Résilience ---
    print("\n" + "=" * 50)
    print("TEST 5: RESILIENCE TESTING")
    print("=" * 50)
    
    # Opération qui réussit
    success_result = system.resilience.execute_with_resilience(
        lambda: "Success!",
        fallback_value="Fallback",
        context="Successful operation"
    )
    print(f"Success test: {success_result.value}")
    
    # Opération qui échoue
    fail_count = [0]
    def failing_operation():
        fail_count[0] += 1
        if fail_count[0] < 4:
            raise Exception("Simulated failure")
        return "Recovered!"
    
    fail_result = system.resilience.execute_with_resilience(
        failing_operation,
        fallback_value="Used fallback",
        max_retries=3,
        context="Failing operation"
    )
    print(f"Failure test: {fail_result.value}")
    
    # --- Rapport Final ---
    print("\n" + "=" * 50)
    print("FINAL SYSTEM REPORT")
    print("=" * 50)
    
    report = system.get_system_report()
    for section, data in report.items():
        print(f"\n[{section.upper()}]")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {data}")
    
    print("\n" + "#" * 70)
    print("#" + " " * 18 + "DEMONSTRATION COMPLETE" + " " * 18 + "#")
    print("#" * 70 + "\n")
    
    return system, report


# Point d'entrée
if __name__ == "__main__":
    system, report = run_demonstration()