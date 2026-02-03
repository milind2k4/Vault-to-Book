
# Chemical Kinetics {#chemical-kinetics}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


Deals with the rate at which reactants are converted into products and also with the effect of variation of conc., temp. etc. on on rate of reaction. 

It is a microscopic study. Thermodynamics is macroscopic study.

#### Rate of Appearance and Disappearance

 Appearance is for products and Disappearance is for reactants.

$$\ce{ 2A + 3B -> C + 2D }$$

Rate of disappearance of A = no of moles of A reacted per unit time per unit volume.
$$\ce{ = - \frac{ d[A]_{t} }{ dt } or - \frac{ \Delta [A] }{ \Delta t } }$$
-ve because concentration is decreasing and thus d[A] is -ve.

Similarly, we can write, rate of appearance of C,
$$\ce{ = \frac{ d [B]_{t} }{ dt } }$$

##### Relation between RoD and RoA

If all substances are in the same phase. 
For the reaction,
$$\ce{ 2A + 3B -> C + 2D }$$

We can write,
$$
\begin{split}
\ce{ 
\frac{ d[C] }{ dt } &= -\frac{ 1 }{ 2 } \frac{ d[A] }{ dt } \\
\frac{ d[D] }{ dt } &= 2 \frac{ d[C] }{ dt } \\
}
\end{split}
$$
$$
\begin{split}
\frac{ d[C] }{ dt }C &= -\frac{ 1 }{ 2 } \frac{ d[A] }{ dt } \\
\frac{ d[D] }{ dt } &= 2 \frac{ d[C] }{ dt } \\
\end{split}
$$
I.e.,
$$\ce{ - \frac{1}{2} \frac{ d[A] }{ dt } = - \frac{1}{3} \frac{ d[B] }{ dt } = \frac{ 1 }{ 1 } \frac{ d[C] }{ dt } = \frac{1}{2} \frac{ d[D] }{ dt } }$$

For a general reaction,
$$\ce{ aA_{(g)} + bB_{(g)} -> cC_{(g)} + dD_{(g)} }$$
We can write,
$$\ce{ - \frac{ 1 }{ a }\frac{ d[A] }{ dt } = - \frac{ 1 }{ b }\frac{ d[B] }{ dt } = \frac{ 1 }{ c }\frac{ d[C] }{ dt } = \frac{ 1 }{ d }\frac{ d[D] }{ dt } }$$

#### Rate of Reaction 

It is defined as the rate of change of conc. of any substance involved in reaction divided by its stoichiometric coefficient in chemical given chemical equation. 

It can be the same or different than the rate of appearance or disappearance of any substance in the reaction. 

$$\ce{ aA + bB -> cC + dD }$$

$$\ce{ Rate = - \frac{ 1 }{ a }\frac{ d[A] }{ dt } = - \frac{ 1 }{ b }\frac{ d[B] }{ dt } = \frac{ 1 }{ c }\frac{ d[C] }{ dt } = \frac{ 1 }{ d }\frac{ d[D] }{ dt } }$$

**Note:** Is stoichiometry of a reaction is altered by multiplying equation by a factor, then rate of reaction is changed. But, rate of disappearance and rate of appearance of a substance does not change. 

**Major factors affecting Rate of Reaction,** 
1. Concentration or Partial Pressure
2. Temperature
3. Catalyst
4. Surface area if solids are involved

## [[02 Kinetics]]

### [[04 Exp. Det. of Order and k of First Order]]

### Parallel or Competing First Order Reaction 

A reaction where A converts to B and C simultaneously, is not parallel.

![](images/Pasted image 20240308184024.png)

A parallel reaction is one where the rate constants are different.

![](images/Pasted image 20240308184039.png)

For a general parallel reaction,

![](images/Pasted image 20240308184308.png)

We have,
$$
\begin{split}
x &= \frac{ y }{ m } + \frac{ z }{ n } \\
\frac{ dx }{ dt } &= \frac{ 1 }{ m }\frac{ dy }{ dt } + \frac{ 1 }{ n }\frac{ dz }{ dt } \\
-\frac{ d[A] }{ dt } &= \frac{ 1 }{ m }mk_{1}[A] + \frac{ 1 }{ n }nk_{2}[A] \\
-\frac{ d[A] }{ dt } &= (k_{1}+k_{2})[A]
\end{split}
$$
Thus the overall rate constant of parallel reaction is,
$$k = k_{1}+k_{2}$$

And the integrated rate law will be,
$$[A]_{t} = [A]_{o} e^{ -(k_{1}+k_{2})t }$$

We can also write this as,
$$\frac{ \ln 2 }{ t_{1/2}\text{(overall)} } = \frac{ \ln 2 }{ t_{1/2(1)} } + \frac{ \ln 2 }{ t_{1/2(2) } }$$

We can also relate activation energy,
$$
\begin{split}
k &= k_{1} + k_{2} \\
Ae^{ -E_{a}/RT } &= A_{1}e^{ -E_{a 1}/RT } + A_{2}e^{ -E_{a 2}/RT } \\
Ae^{ -E_{a}/RT } \frac{ E_{a} }{ RT^{2} } &= A_{1}e^{ -E_{a 1}/RT } \frac{ E_{a 1} }{ RT^{2} } + A_{2}e^{ -E_{a 2}/RT } \frac{ E_{a 2} }{ RT^{2} } \\
kE_{a} &= k_{1}E_{a 1} + k_{2} E_{a 2} 
\end{split}
$$
Thus we get, overall activation energy of parallel reaction,
$$E_{a} = \frac{ k_{1} E_{a 1} + k_{2} E_{a 2} }{ k_{1} + k_{2} }$$

#### Concentration of Products 

$$
\begin{split}
\frac{ d[B] }{ dt } &= mk_{1}[A]_{t} \\
\int d[B]_{t} &= mk_{1}[A]_{o} \int e^{ -(k_{1}+k_{2})t } \, dt \\
[B]_{t} &= \frac{ mk_{1}[A]_{o} }{ k_{1} + k_{2} } (1 - e^{ -(k_{1}+k_{2})t })  
\end{split}
$$

Similarly, we get, conc. of C,
$$[C]_{t} = \frac{ nk_{2}[A]_{o} }{ k_{1} + k_{2} } (1 - e^{ -(k_{1}+k_{2})t })  $$

Thus, at any time, the ratio of conc. of B and C,
$$\frac{ [B]_{t} }{ [C]_{t} } = \frac{ mk_{1} }{ nk_{2} }$$

### First Order Reactions

#### First Order Reversible Reaction 

$$t = \frac{ 1 }{ k_{1} + k_{2} } \ln \frac{ x_{c} }{ x_{c} - x }$$

![](images/Pasted image 20240308201445.png)

#### First Order Sequential Reaction 

aka **Consecutive reaction**

Example is radioactive disintegration series. 
Note than radioactive decay always follows first order kinetics. 

$$\ce{ A -> I -> P }$$

![](images/Pasted image 20240308203216.png)

Then,
$$
\begin{split}
[A]_{t} &= [A]_{o}e^{ -k_{1}t } \\
[I]_{t} &= \frac{ k_{1}[A]_{o} }{ k_{2}-k_{1} } (e^{ -k_{1}t } - e^{ -k_{2}t }) \\
[P]_{t} &= \frac{ [A]_{o} }{ k_{2} - k_{1} } [k_{2}(1-e^{ -k_{1}t }) - k_{1}(1-e^{ -k_{1}t })]
\end{split}
$$

The time at which conc. of intermediate is max is,
$$t_{I_{max}} = \frac{ \ln k_{1} /k_{2} }{ k_{1} - k_{2} }$$


\newpage


# Effect of Concentration {#effect-of-concentration}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


[[01  Law of Mass Action]]

Experimentally, it was found that,
$$\ce{ Rate \propto [A]^{p}[B]^{q} }$$
Thus we can write,
$$\ce{ Rate = k_{r}[A]^{p}[B]^{q} }$$
This equation is called *Rate Law.*

p and q are called partial order wrt A and B and they may or may not be equal to the stoichiometric coefficient of substance. 

$\ce{ k_{r} }$ is the rate constant of reaction and $m = p + q$ is the order of reaction.

#### Order of Reaction 

It is the sum of exponents of all concentration terms appearing in rate law. 
It can be +ve, -ve or zero or fractional. It is determined *experimentally.* It cannot be predicted by just seeing stoichiometry of reaction.

Order reflects the sensitivity of rate of reaction with variation in concentration. 

For example, rate of the below reaction does not depend on concentration,
$$\ce{ H_{2} + Cl_{2} ->[h\nu] 2HCl, Rate = k }$$
$$\ce{ H_{2} + Cl_{2} ->[h\nu] 2HCl, Rate = k }$$

The order of below reaction is first order,
$$\ce{ 2N_{2}O_{5} -> 4NO_{2} + O_{2}, Rate = k[N_{2}O_{5}] }$$

The following reaction is second order,
$$\ce{ 2HI ->[\Delta] I_{2} + H_{2}, Rate = k[HI]^{2} }$$

And the following is zero order,
$$\ce{ 2HI ->[\Delta][gold surface] H_{2} + I_{2}, Rate = k }$$

#### Rate Constant 

Rate constant or velocity constant or specific reaction rate is equal to rate of reaction if all concentrations of substance involved in rate law are set equal to unity. 

Its unit depends on order of reaction.

$$\ce{ k = \frac{ Rate }{ [A]^{p}[B]^{q} } = \frac{ mol l^{-1} s^{-1} }{ [mol l^{-1}]^{p+q} } }$$

Thus, for zero order reaction, unit of k is $\ce{ mol l^{-1} s^{-1} }$. 
Thus, for first order reaction, unit of k is $\ce{ s^{-1} }$. 
Thus, for second order reaction, unit of k is $\ce{ mol^{-1} l s^{-1} }$. 

It increases with temp..

#### Rate constant of Disappearance and Appearance 

We have,
$$\ce{ Rate = - \frac{ 1 }{ a }\frac{ d[A] }{ dt } = - \frac{ 1 }{ b }\frac{ d[B] }{ dt } = \frac{ 1 }{ c }\frac{ d[C] }{ dt } = \frac{ 1 }{ d }\frac{ d[D] }{ dt } }$$

Also,
$$\ce{ Rate = k[A]^{p}[B]^{q} }$$

Thus,
$$\ce{ -\frac{ d[A] }{ dt } = ak[A]^{p}[B]^{q} }$$
$$\ce{ -\frac{ d[A] }{ dt } = k_{A}[A]^{p}[B]^{q} }$$
Where $k_{A} = ak$. 
I.e. 
$$\ce{ k = \frac{ k_{A} }{ a } = \frac{ k_{B} }{ b } = \frac{ k_{C} }{ c } = \frac{ k_{D} }{ d } }$$

Where $\ce{ k_{A}, k_{B}, k_{C}, k_{D} }$ are rate constants for A, B, C, D.

Thus rate constant of reaction may or may not be the same as the rate constant of disappearance or appearance of substance. 


\newpage


# Kinetics {#kinetics}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


### Zero Order Kinetics 
When order of reaction is zero. 

If the reaction is,
$$\ce{ A -> P }$$
Then the rate will be,
$$\ce{ Rate = - \frac{ d[A] }{ dt } = k[A]^{0} = k }$$
This is called *differential rate law.* 

Using it we can find *integrated rate law,*
$$
\begin{split}
- \frac{ d[A] }{ dt } &= k \\
\int_{[A]_{o}}^{[A]_{t}} d[A] &= -k \int_{0}^{t} dt \\
[A]_{o} - [A]_{t} &= kt 
\end{split}
$$
Thus, we get, the integrated rate law,
$$\ce{ [A]_{t} = [A]_{o} - kt }$$

Now, if in t time, x mol/lit are used up from the initial a mol/lit, we can write,
$$
\begin{split}
a - x &= a - kt \\
x &= kt
\end{split}
$$
Where x is the conc. of A or reactant reacted in t time. 
I.e.,
$$\ce{ x = [A]_{o} - [A]_{t} }$$

##### Half Life 

Time in which half of the reactant gets reacted. 

For zero order reaction, 
$$\ce{ [A]_{t} = [A]_{o} - kt }$$
If $t = t_{1 /2}$, $\ce{ [A]_{t} = [A]_{o}/2 }$,
And thus,
$$\ce{ t_{1 /2} = \frac{ [A]_{o} }{ 2k } }$$

**Time of completion** is when reactants become zero. 
$$\ce{ t_{c} = \frac{ [A]_{o} }{ k } = 2t_{1 /2} }$$

Only zero order reaction completes in a finite time period. 

Equal concentrations of reactants react in equal time periods in zero order reaction.

The conc. of reactant remaining after equal time periods forms AP. 

$$
\begin{split}
[A]_{o} &= [A]_{o} \\
[A]_{10} &= [A]_{o} - 10k \\
[A]_{20} &= [A]_{o} - 20k \\
[A]_{30} &= [A]_{o} - 30k \\
\end{split}
$$

#### Graph

![](images/Pasted image 20240307171302.png)

##### Some PTR

Note that if the reaction becomes,
$$\ce{ mA ->[k] P }$$
Then rate of reaction becomes,
$$\ce{ - \frac{ 1 }{ m }\frac{ d[A] }{ dt } = k }$$
Thus the integrated rate law becomes,
$$\ce{ [A]_{t} = [A]_{o} - mkt = [A]_{o} - k_{A}t }$$
And half life becomes,
$$\ce{ t_{1 /2} = \frac{ [A]_{o} }{ 2(mk) } = \frac{ [A]_{o} }{ 2k_{A} } }$$

If the reaction has 2 or more reactants,
$$\ce{ A + 2B ->[k] P }$$
Then,
$$\ce{ [A]_{t} = [A]_{o} - k_{A}t }$$
$$\ce{ [B]_{t} = [B]_{o} - k_{B}t }$$

And half life,
$$\ce{ t_{1 /2(A)} = \frac{ [A]_{o} }{ 2k_{A} } }$$
$$\ce{ t_{1 /2(B)} = \frac{ [B]_{o} }{ 2k_{B} } }$$

Half life of reaction is defined when both the half lives are equal. 
$$
\begin{split}
t_{1 /2(A)} &= t_{1 /2(B)} \\
\frac{ [A]_{o} }{ [B]_{o} } &= \frac{ 1 }{ 2 }
\end{split}
$$

Thus for a reaction involving 2 more reactants, then half lives of all reactants are equal when their initial conc. are taken in their stoichiometric proportions. 

In such case, 
$$t_{1/2(A)} = t_{1 /2(B)} = t_{1 /2(\text{reaction})}$$

### First Order Kinetics 

$$\ce{ A ->[k] P }$$

Differential rate law,
$$\ce{ - \frac{ d[A] }{ dt } = k[A] }$$

Integrated rate law,
$$
\begin{split}
\int_{[A]_{o}}^{[A]_{t}} \frac{ d[A] }{ [A] } &= -k \int_{0}^{t} dt \\
\ln \frac{ [A]_{t} }{ [A]_{o} } &= -kt  \\
[A]_{t} &= [A]_{o} e^{-kt}  
\end{split}
$$

And k can be written as,
$$k = \frac{ 2.303 }{ t } \log_{10} \frac{ [A]_{o} }{ [A]_{t} }$$

Half life is thus,
$$t_{1/2} = \frac{ \ln 2 }{ k } = \frac{ 0.693 }{ k }$$
Which is independent of concentration. 

As we increase temp., k decreases and thus half life decreases. 

Time of completion is infinite. 

For first order, average life,
$$t_{avg} = \frac{ 1 }{ k } \approx 1.44 \times t_{1/2}$$

In n half lives, conc. of reactant remaining,
$$[A]_{t_{1/2}(n)} = \frac{ [A]_{o} }{ 2^{n} }$$

#### Graph

![](images/Pasted image 20240307174015.png)

##### Characteristics of First Order Reaction  

Conc. of reactant which reacts in equal time period goes on decreasing. 

Conc. of reactant remaining after equal time period forms GP.
$$
\begin{split}
[A]_{o} &= [A]_{o} \\
[A]_{10} &= [A]_{o}e^{ -10k } \\
[A]_{20} &= [A]_{o}e^{ -20k } \\
[A]_{30} &= [A]_{o}e^{ -30k } \\
\end{split}
$$

Equal conc. of reactant does not react in equal time. But, equal percentage or fraction of reactant reacts in equal time period.

![](images/Pasted image 20240307174735.png)

![](images/Pasted image 20240307175401.png)
(in 2nd question it is 3/4 not 7/8)

![](images/Pasted image 20240307175902.png)

### [[03 2nd Order Kinetics]]

### nth Order Kinetics
$$\ce{ A ->[k] P }$$
And differential rate law is,
$$\ce{ Rate = -\frac{ d[A] }{ dt } = k[A]^{n} }$$

Integrated rate law,
$$
\begin{split}
-\int_{[A]_{o}}^{[A]_{t}} \frac{ d[A] }{ [A]^{n} } &= k\int_{0}^{t} dt \\
t &= \frac{ 1 }{ k(n-1) } \left( \frac{ 1 }{ [A]_{o}^{n-1} } - \frac{ 1 }{ [A]_{t}^{n-1} } \right)
\end{split}
$$

It is applicable everywhere except first order. 

Half Life,
$$\ce{ t_{1/2} = \frac{ 1 }{ k(n-1) } \left( \frac{ 2^{n-1}-1 }{ [A]_{o}^{n-1} } \right) }$$

Thus, 
$$t_{1/2} \propto \frac{ 1 }{ [A]_{o}^{n-1} }$$


\newpage


# nd Order Kinetics {#nd-order-kinetics}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


#### Single Reactant 
$$\ce{ A ->[k] P }$$

Differential rate law,
$$\ce{ Rate = - \frac{ d[A] }{ dt } = k[A]^{2} }$$

Integrated rate law,
$$
\begin{split}
-\int_{[A]_{o}}^{[A]_{t}} \frac{ d[A] }{ [A]_{o}^{2} } &= k \int_{0}^{t} dt \\
\frac{ 1 }{ [A]_{t} } &= \frac{ 1 }{ [A]_{o} } + kt  
\end{split}
$$

Half life,
$$t_{1/2} = \frac{ 1 }{ k[A]_{o} }$$

Thus in 2nd order reaction, 
$$t_{1/2} \propto \frac{ 1 }{ [A]_{o} } $$

And time of completion is infinite. 

Conc. after equal time period form HP. 

**Graph,**

![](images/Pasted image 20240307180826.png)

#### Two Reactants 

$$\ce{ A + B ->[k] P }$$

Differential rate law,
$$\ce{ -\frac{ d[A] }{ dt } = -\frac{ d[B] }{ dt } = k[A][B] }$$

Integrated rate law
$$
\begin{split}
\ce{ 
- \frac{ d }{ dt }(a-x) &= k(a-x)(b-x) \\
\frac{ dx }{ dt } &= k(a-x)(b-x) \\
 }
\int_{0}^{x} \frac{ dx }{ (a-x)(b-x) } &= k \int_{0}^{t} dt \\
k &= \frac{ 1 }{ t(a-b) } \ln \left( \frac{ a-x }{ b-x } \frac{ b }{ a } \right) 
\end{split}
$$

Thus, we get,
$$t = \frac{ 1 }{ k(a-b) } \ln \frac{ b(a-x) }{ a(b-x) }$$

##### Special Case

If $a \gg b$, then $a-b \approx a$ and $a-x \approx a$.

Thus we can write,
$$
\begin{split}
t &= \frac{ 1 }{ k a } \ln\frac{ ab }{ a(b-x) } \\
t &= \frac{ 1 }{ k' } \ln \frac{ b }{ b-x } \\
t &= \frac{ 1 }{ k' } \ln \frac{ [B]_{o} }{ [B]_{t} } \\
\end{split}
$$

Which is the same equation as that of first order. 
Thus it is first order in B. And thus is called *pseudo first order reaction.*

![](images/Pasted image 20240308105158.png)

##### Pseudo Order Kinetics 

It arises when,
1. Rate law involves catalyst (conc. of catalyst remains constant)
2. Solvent taken in excess 
3. One of the reactant's conc. is taken much higher than the others.

Thus, for reaction,
$$\ce{ A + B ->[k] P }$$
If rate law is,
$$\ce{ Rate = k[A][B] }$$
And $[A]_{o} \gg [B]_{o}$, then $\ce{ [A] }$ is almost constant. And we can write,
$$\ce{ Rate = k'[B] }$$
where $k'$ is called pseudo first order rate constant and thus the reaction becomes effectively first order. 

**Examples of Pseudo First Order Reaction:**
1. Hydrolysis of Alkyl halides. 
	$$\ce{ RCl + H_{2}O ->[k] ROH + HCl }$$
	Here, $\ce{ Rate = k[RCl][H_{2}O] }$. But since water is taken in excess and $\ce{ [H_{2}O] = 55.55 M }$, we get,
	$$\ce{ Rate = k'[RCl], k' = k[H_{2}O] }$$

2. Acid catalysed hydrolysis of sucrose.
	$$\ce{ C_{12}H_{22}O_{11} + H_{2}O ->[H+] \underset{ glucose }{ C_{6}H_{12}O_{6} } + \underset{ fructose }{ C_{6}H_{12}O_{6} } }$$
	
	Experimentally, 
	$$\ce{ Rate = k [C_{12}H_{22}O_{11}][H_{2}O][H+] }$$
	However, $\ce{ H_{2}O }$ is solvent and $\ce{ H+ }$ is catalyst. 
	Thus, the rate law becomes,
	$$\ce{ Rate = k'[C_{12}H_{22}O_{11}] }$$

\newpage


# Exp. Det. of Order and k of First Order {#exp-det-of-order-and-k-of-first-order}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


### Exp. Det. of Order of Reaction 
Order of reaction cannot be determined by seeing the stoichiometric of reaction. 

If reaction is an elementary reaction, or single step reaction, then order of reaction is the sum of stoichiometric coefficients of reactants.

![](images/Pasted image 20240308111402.png)

However, we cannot find if a reaction is elementary or not just by see the reaction. 

#### Initial Rate Method 

We determine rates at various conc. of the reactants. From this we can find the order.

![](images/Pasted image 20240308111654.png)

#### Half Life Method 

We know that, for an nth order reaction,
$$t_{1/2} \propto \frac{ 1 }{ a^{n-1} }$$
where a is initial concentration of  reactant.

n represents the order of reaction and we cannot find partial order from this method.

![](images/Pasted image 20240308112032.png)

#### Hit and Trial Method 

This is also called **Integrated Rate Law Method.**

![](images/Pasted image 20240308113632.png)

### Monitoring the Progress of 1st Order Reaction

i.e. Determination of  rate constant, k.

There are 3 methods,
1. Pressure Measurement 
2. Titration 
3. Optical rotation measurement 

#### By Pressure Measurement 

Applicable reaction involving at least one gas. 

For constant V and T,
$$p \propto c$$

Thus we can write,
$$
\begin{split}
k &= \frac{ 1 }{ t } \ln \frac{ [A]_{o} }{ [A]_{t} } \\
&= \frac{ 1 }{ t } \ln \frac{ a }{ a-x } \\
&= \frac{ 1 }{ t } \ln \frac{ p_{o(A)} }{ p_{t(A)} }
\end{split}
$$

![](images/Pasted image 20240308114608.png)

A general formula is,
$$k = \frac{ 1 }{ t } \ln \frac{ p_{\infty} - p_{o} }{ p_{\infty} - p_{t} }$$

![](images/Pasted image 20240308115920.png)

#### By Titration 

[[02 Equivalent Concept#Law of Chemical Equivalence]]

The rate constant will be found directly in term of volumes of titrant used at various instances of the reaction. 

$$k = \frac{ 1 }{ t } \ln \frac{ V_{o} }{ V_{t} }$$

![](images/Pasted image 20240308120743.png)

![](images/Pasted image 20240308121319.png)

#### By Measurement of Optical Rotation

[[06 Optical Isomerism#Checking Optical Activity]]

This is applicable only for reaction involving optically active compounds.

Optical rotation $\theta$, 
$$
\begin{split}
\theta &\propto \text{conc.} \\
&\propto \text{thickness of polarimeter tupe (t)}
\end{split}
$$
The thickness t is taken as 1 because it cancels out in the ratio inside log in case of first order kinetics. 

We can write,
$$\theta = r \times c$$
where, 
$r \to$ *specific rotation of compound.* It is constant for an optically active compound.
$c \to$ concentration of solution wrt that compound. 
$\theta \to$ observed rotation. 

The general formula for the rate constant comes out to be,
$$k = \frac{ 1 }{ t } \ln \frac{ \theta_{\infty} - \theta_{o} }{ \theta_{\infty} - \theta_{t} }$$
It is applicable for any first order with optically active compound.

![](images/Pasted image 20240308122421.png)

![](images/Pasted image 20240308172212.png)

\newpage


# Effect of Temperature {#effect-of-temperature}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


It is observed that rate of reaction becomes double to triple for every 10 K rise in temp. for most chemical reactions.

### Collision Theory

If a reaction has to proceed in the forward direction, the reactants must collide with each other. 

Every collision is not successful.  

For a collision to be successful to form products, reactants must possess a certain min. total energy called **Threshold Energy** and also have proper orientation. 

**Activation Energy** is the additional KE possessed by reactants relative to initial state of reactants to cross energy barrier (TS).

![](images/Pasted image 20240308173034.png)

![](images/Pasted image 20240308173614.png)

Rate of reaction is given as,
Rate of Reaction = collision frequency $\times$ energy barrier factor $\times$ orientation factor

*Orientation factor* is also known as *steric factor or probability factor.*

*Collision frequency* is no. of collisions per unit volume per unit time.

*Energy barrier factor* is $e^{ -E_{a}/RT }$ and it represents the fraction of reactant molecules that have KE more than or equal to activation energy $E_{a}$.

##### Arrhenius Equation

Finally, the rate of reaction comes out to be,
$$\ce{ Rate = (Ae^{ -E_{a}/RT }) (conc.)^{order} }$$

This is written as,
$$\ce{ Rate = k (conc.)^{order} }$$
where k is rate constant for reaction and,
$$\ce{ k = Ae^{ -E_{a}/RT } }$$
This equation is called **Arrhenius Equation.**
Here,
$E_{a} \to$ activation energy of reaction 
$A \to$ frequency factor or *Arrhenius constant.* 
$T \to$ temp. in kelvin.

![](images/Pasted image 20240308175001.png)

Both $\ce{ E_{a} and A }$ are taken to be independent of temp..

The max. value of k becomes A when,
1. $T \to \infty$
2. $E_{a} = 0$ i.e. no energy barrier. 

A is the product of collision frequency and orientation factor. 
$$A = Z_{11}\times p$$

We have,
$$
\begin{split}
k &= Ae^{ -E_{a}/RT } \\
\ln k &= \ln A - \frac{ E_{a} }{ RT }
\end{split}
$$
And thus the graph will look like,

![](images/Pasted image 20240308175144.png)

##### Integral and Differential form of A. Equation 

Applying the log equation at two temp., we can find the integral form of the Arrhenius equation.

At temp. $T_{1}$,
$$\ln k_{1} = \ln A - \frac{ E_{a} }{ RT_{1} }$$
At temp. $T_{2}$,
$$\ln k_{2} = \ln A - \frac{ E_{a} }{ RT_{2} }$$

Subtracting them,
$$
\begin{split}
\ln \frac{ k_{1} }{ k_{2} } &= \frac{ E_{a} }{ R } \left( \frac{ 1 }{ T_{1} } - \frac{ 1 }{ T_{2} } \right) \\
\\
\log_{10} \frac{ k_{1} }{ k_{2} } &= \frac{ E_{a} }{ 2.303R } \left( \frac{ 1 }{ T_{1} } - \frac{ 1 }{ T_{2} } \right)
\end{split}
$$
This is called the integral form of Arrhenius equation.

Now, differentiating the log equation wrt T,
$$
\begin{split}
\ln k &= \ln A - \frac{ E_{a} }{ RT } \\
\frac{ d(\ln k) }{ dT } &= -\frac{ E_{a} }{ R } \left( -\frac{ 1 }{ T^{2} } \right) \\
\frac{ d(\ln k) }{ dT } &= \frac{ E_{a} }{ RT^{2} }
\end{split}
$$

The reaction which has greater $E_{a}$ will be more sensitive towards temp. variation. 

Rate constant of reaction increases more sharply for a reaction at lower temp. than at higher temp. for same temp. rise.

![](images/Pasted image 20240308180406.png)

##### Why Rate Constant becomes 2x to 3x for every 10K rise in temp.

[[00 KTG & Thermodynamics#Maxwell Boltzmann Distribution]]

Note that the average KE does not change much, but the fraction of molecules having more energy than $E_{a}$ is increased.

![](images/Pasted image 20240308181008.png)

### Reversible Reactions 

$$\ce{ A <=>[E_{af}, k_{f}][E_{ab}, k_{b}] B }$$

At eqilibrium,
$$\ce{ k_{eq} = \frac{ [B]_{eq} }{ [A]_{eq} } = \frac{ k_{f} }{ k_{b} } }$$

![](images/Pasted image 20240308181253.png)

From the graph, we can see that,
$$\Delta H_{r} = E_{af} - E_{ab}$$

Now,
$$
\begin{split}
k_{eq} &= \frac{ A_{f}e^{ -E_{af}/RT } }{ A_{b}e^{ -E_{ab}/RT } } \\
&= \frac{ A_{f} }{ A_{b} } e^{ -(E_{af} - E_{ab})/RT } \\
&= \frac{ A_{f} }{ A_{b} } e^{ -\Delta H_{r}/RT } \\
\ln k_{eq} &= \ln \frac{ A_{f} }{ A_{b} } - \frac{ \Delta H_{r} }{ RT } \\
\frac{ d(\ln k_{eq}) }{ dT } &= \frac{ \Delta H_{r} }{ RT^{2} }
\end{split}
$$
This is the differential form of [[02 Characteristics of Equilibrium Constant#Van't Hoff Equation|Von't Hoff Equation.]]

And its integral form will be,
$$
\begin{split}
\ln \frac{ k_{eq 1} }{ k_{eq 2} } &= \frac{ \Delta H_{r} }{ R } \left( \frac{ 1 }{ T_{1}^{2} } - \frac{ 1 }{ T_{2}^{2} } \right) \\
\\
\log_{10} \frac{ k_{eq 1} }{ k_{eq 2} } &= \frac{ \Delta H_{r} }{ 2.303R } \left( \frac{ 1 }{ T_{1}^{2} } - \frac{ 1 }{ T_{2}^{2} } \right) 
\end{split}
$$

As temp. increases Rate constant increases always. Irrespective of whether reaction if endothermic or exothermic. 

But, as temp. increases equilibrium constant increases for endothermic and decreases for exothermic.

\newpage


# Effect of Catalyst and Surface Area {#effect-of-catalyst-and-surface-area}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


### Effect of Catalyst 
Catalyst is added into the reaction mixture in small amount which without being consumed alters the mechanism of reaction and takes the reaction through alternate path involving lower activation energy and hence reaction becomes faster. 

Catalyst does not effect,
- Equilibrium constant 
- Thermodynamic parameters

Catalyst decreases the value of $E_{a}$ both forward and backward reaction by the same amount and hence $k_{f}$ and $k_{b}$ are increased by same factor. 

Catalyst cannot turn a non spontaneous reaction into a spontaneous one.

![](images/Pasted image 20240308182821.png)

For catalysed path,
$$
\begin{split}
k_{f}' &= A_{f}e^{ -(E_{af}-x)/RT } \\
k_{b}' &= A_{b}e^{ -(E_{ab}-x)/RT } \\
k_{eq}' &= \frac{ A_{f} }{ A_{b} } e^{ -(E_{ab} - E_{af})/RT } \\
k_{eq}' &= \frac{ A_{f} }{ A_{b} } e^{ -\Delta H_{r}/RT } \\
&= k_{eq}
\end{split}
$$

### Effect of Surface Area 

Only applies to reactions which occur through adsorption on solid surface.

As surface area increases, rate of reaction increases. 

A solid in powdered or porous form has high surface area and hence high rate of reaction.

\newpage


# Mechanism and Order from Mechanism {#mechanism-and-order-from-mechanism}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


### Mechanism of Reaction 
The various steps involved in conversion of reactants into products in a chemical reaction. 

##### Molecularity 

It is the no. of reactant molecules that form TS and finally convert into product. 
  
It is defined for a step of a complex reaction or defined for an elementary reaction.  

It is usually 1, 2 or rarely 3 but not found to be greater than 3 as probability of 4 or more molecules colliding is very low. 

It cannot be fractional, -ve or zero. 

Molecularity of 1 means *unimolecular* reaction, 2 means *bimolecular* reaction and 3 means *trimolecular* reaction. 

For an elementary reaction, molecularity is equal to order of reaction which is equal to sum of stoichiometric coefficients of reactants. 

This indicates that zero order reaction is a complex reaction.

#### Types of Reaction

There are two types of reaction based on mechanism,

##### Elementary

Which complete in one step. No intermediate is involved. 
   
The given reaction or step is **Rate Determining Step (RDS).** It is the slowest step in a reaction.

![](images/Pasted image 20240308203736.png) 

##### Complex 

Which completes in 2 or more steps. 
Slowest step is RDS.
Involves at least one intermediate.

![](images/Pasted image 20240308204922.png)

### Order from given Mechanism 

##### Elementary Reaction 
Given step (reaction) is RDS. 

$$\ce{ A + 2B -> P }$$
$$\ce{ Rate = k[A][B]^{2} }$$
And thus order is 1 + 2 = 3. 

##### More than one step and one of them is Slow

The slow step is RDS. 

We write rate law of the slow step taking it to be elementary. The order comes from this rate law.

![](images/Pasted image 20240308205322.png)

##### Intermediate in Equilibrium with Reactants 

Equilibrium is always fast. 
Equilibrium involves 2 reactions, forwards and backwards.

We write rate law from the slow step and if there are intermediates involved, we remove that as in final rate law conc. of intermediate cannot come. 

The order is obtained from the final rate law.

![](images/Pasted image 20240308205827.png)

##### Info. of Fast/Slow steps are not given 

We apply steady state approximation (SSA). 
All the steps of the reaction are assumed to proceed with the same rate. 

SSA on intermediate gives,
$$\frac{ d[I]_{t} }{ dt } = 0$$

![](images/Pasted image 20240308210556.png)

In photochemical reaction, rate of reaction is proportional to intensity of light absorbed.

![](images/Pasted image 20240308211020.png)



\newpage


# Nuclear Chemistry {#nuclear-chemistry}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}


aka **Radioactivity**

Radioactivity is the spontaneous decay of nuclei of some isotopes of elements to emit $\alpha,\beta,\upgamma$ rays. 

Radioactive decay follows first order kinetics but Arrhenius equation is not applicable as rate of radioactive decay is independent of temp., free or combined form (e.g. U or $\ce{ UF_{6} }$)

In nuclear reaction the reacting element is changed. It does not involve e but rather nuclei. 

Rate of radioactive decay,
$$\ce{ Rate \propto N_{t} }$$
where $N_{t}$ is the no. of nuclei present at time t. 

$$
\begin{split}
-\frac{ dN_{t} }{ dt } &\propto N_{t} \\
-\frac{ dN_{t} }{ dt } &= \lambda N_{t} \\
\end{split}
$$

$\lambda$ is called **decay constant** and it has unit $s ^{-1}$,
$- dN_{t} /dt$ is called **rate of decay or radioactivity or activity.**

Since no. of nuclei is equal to the no. of atoms, we can write,
$$- \frac{ dN_{t} }{ dt } = \lambda N_{t} = \lambda \frac{ W }{ M }N_{A}$$
where,
$W \to$ mass of radioactive substance
$M \to$ molar mass
$N_{A} \to$ Avogadro no.

The SI unit of rate of decay or activity is **dps i.e. disintegration per second.**
But the most commonly used unit is **Curie.**
$$\ce{ 1 Ci = 3.7 \times 10^{10} dps }$$

**Specific Activity** is the activity per unit mass. 

No. of nuclei after time t,
$$
\begin{split}
- \frac{ dN }{ dt } &= \lambda N \\
\int \frac{ dN }{ N } &= \lambda \int dt \\
N_{t} &= N_{o} e^{ -\lambda t }  
\end{split}
$$

Decay constant,
$$\lambda = \frac{ 1 }{ t } \ln \frac{ N_{o} }{ N_{t} }$$

Half life,
$$t_{1/2} = \frac{ \ln 2 }{ \lambda } = \frac{ 0.693 }{ \lambda }$$
Average life,
$$t_{avg} = \frac{ 1 }{ \Lambda }$$

No. of nucleoids remaining after x half lives,
$$= \frac{ N_{o} }{ 2^{x} }$$

**Parallel Decay:** [[00 Chemical Kinetics#Parallel or Competing First Order Reaction|Parallel First Order Reaction]]

![](images/Pasted image 20240308213232.png)

#### Radioactive Equilibrium 

Observed in sequential decay. 

$$\ce{ A ->[\lambda_{1}] B ->[\lambda_{2}] C ->[\lambda_{3}] D \dots  }$$

A is the parent element which is radioactive. 
B, C and D are intermediates.

At radioactive equilibrium, rate of formation of B is equal to rate of decay of B. This is SSA. 

$$\ce{ \lambda_{1}N_{A} = \lambda_{2}N_{B} }$$
This is the equation for radioactive equilibrium.

![](images/Pasted image 20240308215331.png)

#### Symbols of Some Important Nuclear Particles 

$$
\begin{split}
\ce{ 
{}_{2}He^{4} &: \alpha-particle \\
\\
{}_{-1}e^{0} &: \beta-particle \\
{}_{+1}e^{0} &: Positron \\
\\
{}_{1}H^{1} &: Proton \\
{}_{1}H^{2} &: Deutron \\
{}_{1}H^{3} &: Triton \\
\\
\upgamma\ or h\nu &: \upgamma-radiation
 }
\end{split}
$$

**$\alpha$ decay:**
$$\ce{ {}_{Z}X^{A} -> {}_{Z-2}Y^{A-4} + {}_{2}He^{4} }$$

**$\beta$ decay:**
$$\ce{ {}_{Z}X^{A} -> {}_{Z+1}P^{A} + {}_{-1}e^{0} }$$

#### Applications of Radioactivity 

##### Rock dating (or Helium dating)
To determine age of rocks/minerals/ores. 

The basis is $\alpha$ particle decay. 

He dating assumes that all $\alpha$ particles produced in the decay are trapped in the ore as He gas.

![](images/Pasted image 20240308220317.png)

##### Carbon dating 

To determine age of fossils, wood, artefacts. 
Mainly used to determine age of dead trees/animals. 

The N in the upper atmosphere captures neutron and forms radioactive carbon, $\ce{ {}_{6}C^{14} }$. This C has half life of its decay of nearly 5770 years. 

This radioactive C is diffused into the lower atmosphere and then goes into the bodies of living organisms. 

A radioactive equilibrium is established in the body. 
Rate of absorption of $\ce{ C^{14} }$ = Rate of decay of $\ce{ C^{14} }$.

There is a constant conc. of $\ce{ C^{14} }$ in the body of alive body. 
After the death of the body, the absorption stops and the decay continues.

$$\ce{ {}_{6}C^{14} -> {}_{7}N^{14} + {}_{-1}e^{0} }$$

The age comes out to be,
$$t_{age} = \frac{ 1 }{ \lambda } \ln \frac{ [C^{14}]_{o} }{ [C^{14}]_{t} }$$
where $\ce{ [C^{14}]_{t} }$ is the conc. in dead animal and $\ce{ [C^{14}]_{o} }$ is the conc. in the alive animal which is approximated on the basis of currently living animals.

\newpage

