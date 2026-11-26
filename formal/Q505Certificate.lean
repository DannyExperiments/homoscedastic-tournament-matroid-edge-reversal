import Std

/-! A three-coordinate certificate for edge reversal. Free edge parameters are
entries of Λ. The two matrices in the paper are I − Λ. We use rows 1 and 3
only, since they determine the selected entries of s (I − Λ)(I − Λ)ᵀ. -/
namespace TournamentWitness
open Lean.Grind

abbrev Triple (R : Type) := R × R × R

def dot {R : Type} [CommRing R] (u v : Triple R) : R :=
  u.1*v.1 + u.2.1*v.2.1 + u.2.2*v.2.2

def projection {R : Type} [CommRing R] (s : R) (r₁ r₃ : Triple R) : Triple R :=
  (s*dot r₁ r₁, s*dot r₁ r₃, s*dot r₃ r₃)

def separator {R : Type} [CommRing R] (v : Triple R) : R :=
  v.1*v.2.2 - v.2.1*v.2.1 - v.2.2*v.2.2

def cycle {R : Type} [CommRing R] (s b c : R) : Triple R :=
  (s*(1+b*b), -s*b, s*(1+c*c))

theorem dagIdentity {R : Type} [CommRing R] (s b : R) :
    separator (projection s (1,0,-b) (0,0,1)) = 0 := by
  simp [separator, projection, dot] <;> grind

theorem cycleCoordinates {R : Type} [CommRing R] (s b c : R) :
    projection s (1,0,-b) (0,-c,1) = cycle s b c := by
  simp [projection, dot, cycle] <;> grind

theorem cycleValue {R : Type} [CommRing R] (s b c : R) :
    separator (cycle s b c) = s*s*c*c*(b*b-1-c*c) := by
  simp [cycle, separator] <;> grind

def linearTerm {R : Type} [CommRing R] (s b c ds db dc : R) : Triple R :=
  ((1+b*b)*ds+2*s*b*db, -b*ds-s*db, (1+c*c)*ds+2*s*c*dc)

/-- An exact polynomial expansion identifies the three linear coefficients. -/
theorem linearization {R : Type} [CommRing R] (s b c ds db dc t : R) :
    let u := cycle s b c
    let v := linearTerm s b c ds db dc
    ∃ w : Triple R, cycle (s+t*ds) (b+t*db) (c+t*dc) =
      (u.1+t*v.1+t*t*w.1, u.2.1+t*v.2.1+t*t*w.2.1, u.2.2+t*v.2.2+t*t*w.2.2) := by
  refine ⟨(s*db*db+2*ds*b*db+t*ds*db*db, -ds*db, s*dc*dc+2*ds*c*dc+t*ds*dc*dc), ?_⟩
  simp [cycle, linearTerm] <;> grind

def detCols {R : Type} [CommRing R] (i j k : Triple R) : R :=
  i.1*(j.2.1*k.2.2-j.2.2*k.2.1) - j.1*(i.2.1*k.2.2-i.2.2*k.2.1)
    + k.1*(i.2.1*j.2.2-i.2.2*j.2.1)

def selectedMinor {R : Type} [CommRing R] (s b c : R) : R :=
  detCols (linearTerm s b c 1 0 0) (linearTerm s b c 0 1 0) (linearTerm s b c 0 0 1)

theorem minorFormula {R : Type} [CommRing R] (s b c : R) :
    selectedMinor s b c = 2*s*s*c*(b*b-1) := by
  simp [selectedMinor, detCols, linearTerm] <;> grind

theorem rationalWitness :
    separator (cycle (1 : Rat) (1/4) (1/2)) = -19/64 ∧
    selectedMinor (1 : Rat) (1/4) (1/2) = -15/16 ∧
    (1 : Rat) - (1/4)*(1/4)*(1/2) = 31/32 := by
  rw [cycleValue, minorFormula]
  decide +kernel

#print axioms dagIdentity
#print axioms cycleCoordinates
#print axioms cycleValue
#print axioms linearization
#print axioms minorFormula
#print axioms rationalWitness
end TournamentWitness
