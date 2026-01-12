
# Alternating Current {#alternating-current}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}
When the direction of current is fixed, it is called direct. 

In Alternating current, the direction of current changes many times a second. 
Thus the source also changes polarity.

![](images/Pasted image 20240121173851.png)

#### Sinusoidal AC
$$i = i_{o}\sin \omega t$$
$i$ varies from $[-i_{o},i_{o}]$ and $i_{o}$ is called peak current or current amplitude.
$\omega$ is angular frequency, 
$$\omega = 2 \pi f = \frac{2\pi}{T}$$

Anything inside of sin is called phase. 

As $i$ is varying sinusoidally $V$ also varies sinusoidally.
$$V = V_{o} \sin \upomega t$$

![](images/Pasted image 20240121174324.png)

##### Average Current 
$$i_{avg} = \frac{ \Delta q }{ \Delta t } = \frac{ \smallint i(t)dt }{ \Delta t }$$

![](images/Pasted image 20240121175244.png)

##### RMS value of AC
Root mean Square Value.

First square, then take mean, then take root.

It is the effective value of AC. If nothing is said, assume the value to be rms. 

$$i_{rms} = \sqrt{ \frac{ \int i^{2} \, dt  }{ \int dt  } }$$

Let the current be,
$$i = i_{o}\sin (\omega t + \theta)$$
Now, we find RMS value of this current from t=0 to t=T. 
This value will be the same for $t = 0 \to 2T, 0 \to 3T$ etc. 

$$i_{rms} = \sqrt{ \frac{ \int_{0}^{2\pi/\omega} i^{2} \sin ^{2}(\omega t + \theta) \, dt  }{ \int_{0}^{2\pi/\omega} dt } }$$

And finally, we get,
$$i_{rms} = \frac{i_{o}}{\sqrt{ 2 }}$$

![](images/Pasted image 20240121181835.png)

The rms value is shown in the circuit. A hot wire ammeter measures rms current.

![](images/Pasted image 20230107180223.png)

If current is given as the sum of 2 other sinusoidal out-of-phase currents,

$$i = i_{1}\sin\upomega t + i_{2}\sin(\upomega t + \theta)$$

$$
\begin{split}
i_{rms} &= \sqrt{ \left( \frac{ i_{1} }{ \sqrt{ 2 } } \right)^{2} +  \left( \frac{ i_{2} }{ \sqrt{ 2 } } \right)^{2} + 2. \frac{ i_{1} }{ \sqrt{ 2 } }. \frac{ i_{2} }{ \sqrt{ 2 } } \cos \theta } \\
\\
i_{rms} &= \sqrt{ i_{1rms}^{2} + i_{2rms}^{2} + 2i_{1rms}i_{2rms}\cos \theta }
\end{split}
$$
Which is just like addition of vectors.

![](images/Pasted image 20240121182330.png)

![](images/Pasted image 20240121182529.png)

## Power of Source of Load
[[04 Power]]

Let the current and voltage be,
$$i= i_{o}\sin \omega t$$
$$V = V_{o}(\sin\omega t + \theta)$$

At any instant,
$$
\begin{split}
P &= Vi \\
&= i_{o} V_{o} \sin(\omega t + \theta) \sin \omega t \\
&= \frac{ i_{o}V_{o} }{ 2 } [\cos \theta - \cos (2\omega t + \theta)] \\
&= \frac{ i_{o}V_{o} }{ 2 } \cos \theta - \frac{ i_{o}V_{o} }{ 2 } \cos (2\omega t + \theta) 
\end{split}
$$

Thus,

![](images/Pasted image 20240121183246.png)

Now, average power,
$$
\begin{split}
P_{avg} &= \frac{ i_{o}V_{o} }{ 2 }\cos \theta \\
&= \frac{ i_{o} }{ \sqrt{ 2 } }. \frac{ V_{o} }{ \sqrt{ 2 } } \cos \theta \\
&= i_{rms} . V_{rms}\cos \theta 
\end{split}
$$
Here, $\theta$ is the *power factor angle* or the *phase difference* between i and V. And $\cos \theta$ is called the power factor. 

## AC Generator
It converts mechanical energy into electrical energy. 

It works on the principle that when a loop is moved in a magnetic field, an emf is generated in it. 


When the coil is rotated with constant angular speed $\upomega$, the angle between $\vec{B}$ and $\vec{A}$ is,
$$\theta = \upomega t$$
Now, magnetic flux,
$$\phi = BAN\cos\upomega t$$
From Faraday's laws, induced emf,
$$\varepsilon = -N \frac{ d\phi }{ dt }$$

Thus,
$$\varepsilon = -NBA\upomega \sin\upomega t$$
$\varepsilon = NBA\upomega$ is the max amount of emf that can be produced. 

Dividing it by $R$,
$$i = i_{o} \sin \upomega t$$

In India,
$$
\begin{split}
\varepsilon_{o} &= 220\sqrt{ 2 }\ V \\
\varepsilon_{rms} &= 220\ V \\
f &= 50\ Hz \\
\omega &= 100\pi
\end{split}
$$

![](images/Pasted image 20240121174954.png)

![](images/AC Generator.png)


\newpage


# Individual Circuits {#individual-circuits}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}
## Purely Resistive Circuit

![](images/Pasted image 20240121183610.png)

Applying KVL,
$$
\begin{split}
V_{o}\sin\omega t - iR &= 0 \\
i &= \frac{ V_{o} }{ R } \sin\omega t \\
&= i_{o} \sin\omega t
\end{split}
$$
Thus,
$$i_{o} = \frac{V_{o}}{R}$$

Since voltage and current are in the same phase, we have the phasor diagram,

![](images/Pasted image 20240121183906.png)

Here,
$$\theta = 0 \implies \cos \theta = 1$$
i.e. Power Factor = 1

$$
\begin{split}
P_{avg} &= V_\text{rms}. i_\text{rms} \cos 0 \\
&= \frac{ V_{o} }{ \sqrt{ 2 } }. \frac{ i_{o} }{ \sqrt{ 2 } } . 1 \\
&= \frac{V_\text{rms}^{2}}{R} \\
&= \frac{ i_{o}^{2}R }{ 2 } 
\end{split}
$$

## Purely Capacitive Circuit

![](images/Pasted image 20240121184137.png)

At any time, charge on capacitor,
$$q = CV_{o} \sin\omega t$$

Differentiating this, we get current,
$$
\begin{split}
i &= \upomega C V_{o}\cos\omega t \\
i &= \frac{V_{o}}{\frac{1}{\omega C}} \cos\omega t \\
i &= \frac{V_{o}}{X_{C}} \sin(\omega t+90^{\circ})
\end{split}
$$
here, $X_{C}$ is called **capacitive reactance.** It is the effective resistance provided by a capacitor in an ac circuit. Its unit is ohm. 

$$X_{C} = \frac{ 1 }{ \omega C } = \frac{ 1 }{ 2\pi fC }$$

And,
$$
\begin{split}
i_{o} &= \frac{ V_{o} }{ X_{C} } \\
i_{rms} &= \frac{V_{o}}{\sqrt{ 2 }X_{C}}
\end{split}
$$

In a capacitive circuit, current is ahead of voltage by a phase angle of $\frac{\pi}{2}$. 
Thus the power factor is $\cos 90^{\circ} = 0$, and the average power comes out to be zero in a cycle. 

In the first half, the capacitor charged (acting like a load), and in the next half it discharges (acting like a source). Thus making the net energy stored or dissipated in one cycle, zero.

![](images/Pasted image 20240121184444.png)

## Purely Inductive Circuit

![](images/Pasted image 20240121184820.png)

Using KVL,
$$
\begin{split}
V_{o}\sin\omega t - L \frac{ di }{ dt } &= 0 \\
i &= \frac{ -V_{o} }{ \omega L } \cos\omega t \\
&= \frac{ V_{o} }{ X_{L} } \sin (\omega t - 90^{\circ})
\end{split}
$$
Here, $X_{L}$ is called**inductive reactance.** It is the effective resistance provided by an inductor in an ac circuit. Its unit is ohm. 
$$X_{L} = \omega L = 2\pi fL$$

And,
$$
\begin{split}
i_{o} &= \frac{ V_{o} }{ X_{L} } \\
i_\text{rms} &= \frac{V_{o}}{\sqrt{ 2 }X_{L}}
\end{split}
$$

In an inductive circuit, current is behind voltage by a phase angle of $\frac{\pi}{2}$. 
Thus the power factor is $\cos 90^{\circ} = 0$, and the average power is zero for a cycle. 

For half a cycle current and magnetic energy increases (acting like a source) and for the next half, both will decrease (acting like a source).

![](images/Pasted image 20240121185352.png)

\newpage


# Dual Circuits {#dual-circuits}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}
Impedance is effective resistance (i.e. reactance + resistance) of circuit and is represented by Z.

## RC Circuit

![](images/Pasted image 20240121185451.png)

Applying KVL,
$$
\begin{split}
V - V_{R} - V_{C} &= 0 \\
V_{R} + V_{C} &= V
\end{split}
$$

We add the voltages using phasors, taking the current as base. 
$$V = i\sqrt{ R^{2} + X_{C}^{2} }$$

Thus we get impedance,
$$Z = \sqrt{ R^{2} + X_{C}^{2} }$$
And peak current,
$$i_{o} = \frac{ V_{o} }{ Z } = \frac{ V_{o} }{ \sqrt{ R^{2} + X_{C}^{2} } }$$

![](images/Pasted image 20240121185746.png)

From the phasor, we can see that current is ahead of voltage by a phase of,
$$\theta = \cos ^{-1} \frac{ R }{ Z }$$

Now, power factor,
$$
\begin{split}
\cos \theta &= \frac{ V_{R} }{ V } \\
&= \frac{ iR }{ iZ } \\
&= \frac{ R }{ Z }
\end{split}
$$

And thus, the average power,
$$
\begin{split}
P_{avg} &= i_{rms}V_{rms} \cos \theta \\
&= i_{rms}^{2}R 
\end{split}
$$

![](images/Pasted image 20240121190615.png)


## LR Circuit

![](images/Pasted image 20240121190634.png)

Applying Kirchhoff's Loop Law,
$$V = V_{R} + V_{L}$$

Adding them using phasors, with current as base,

$$V = i\sqrt{ R^{2} + X_{L}^{2} }$$
Thus, impedance,
$$Z = \sqrt{ R^{2} + X_{L}^{2} }$$
And peak current,
$$i_{o} = \frac{ V_{o} }{ Z }$$
RMS current,
$$i_{rms} = \frac{ V_{rms} }{ Z }$$

![](images/Pasted image 20240121190643.png)

From here, we see that current is lagging voltage by angle,
$$\theta = \cos ^{-1} \frac{ R }{ Z }$$

Now, power factor,
$$
\begin{split}
\cos \theta &= \frac{ V_{R} }{ V } \\
&= \frac{ iR }{ iZ } \\
&= \frac{ R }{ Z }
\end{split}
$$

Thus, we get average power,
$$
\begin{split}
P_{avg} &= i_{rms} V_{rms} \cos \theta \\
&= i^{2}_{rms} R 
\end{split}
$$

 **Choke Coil:** It is a wire with many loops. Thus it is kind of an inductor. 

They have resistance as well as inductance. An ideal choke coil has no resistance. 

Thus, we can consider choke coil to be inductor.

![](images/Pasted image 20240121191221.png)

![](images/Pasted image 20240121191515.png)


## LC Circuit
[[04 Circuit Solutions of LR Circuit#LC Oscillations]]

![](images/Pasted image 20240121191527.png)

Applying Kirchhoff's Loop Law,
$$V = V_{L} + V_{C}$$

Adding them using phasors, with current as the base,
$$V = i|X_{L} - X_{C}|$$

Thus, impedance,
$$Z = |X_{L} - X_{C}|$$
And peak current,
$$i_{o} = \frac{ V_{o} }{ Z }$$
RMS current,
$$i_{rms} = \frac{ V_{rms} }{ Z }$$

![](images/Pasted image 20240121191606.png)

From here we can see that the phase difference between current and voltage in an LC circuit is always 90.

**If $X_{L} > X_{C}$,** the circuit is called **Inductive.**

Thus,
$$
\begin{split}
\omega L &> \frac{ 1 }{ \omega C } \\
\omega &> \frac{ 1 }{ \sqrt{ LC } }
\end{split}
$$
And we get,
$$Z = X_{L} - X_{C}$$

Current is lagging behind voltage by a phase of $\frac{\pi}{2}$.

Since $\cos \theta = 0$, average power comes out to be zero.

![](images/Pasted image 20240121192029.png)

**If $X_{C} > X_{L}$,** the circuit is called Capacitive. 

Thus,
$$
\begin{split}
\omega L &< \frac{ 1 }{ \omega C } \\
\omega &< \frac{ 1 }{ LC }
\end{split}
$$
And we get,
$$Z = X_{C} - X_{L}$$

Current is ahead of the voltage by a phase of $\frac{\pi}{2}$. 

Since power factor is zero, $\cos \theta = 0$, the average power is zero. 

#### Graphs for LC circuit

In Z vs $\omega$ curve,

$$
\begin{split}
Z &= |X_{L} - X_{C}| \\
&= \left| \omega L - \frac{ 1 }{ \omega C } \right| 
\end{split}
$$

Similarly, we have $i_{rms}$ vs $\omega$,
$$
\begin{split}
i_{rms} &= \frac{ V_{rms} }{ Z } \\
&= \frac{ V_{rms} }{ \left| \omega L - \frac{ 1 }{ \omega C }\right| }
\end{split}
$$

And thus we get, $\omega$ resonance, 
$$
\begin{split}
\omega_{r} &= \frac{ 1 }{ \sqrt{ LC } } \\
f_{r} &= \frac{ 1 }{ 2\pi \sqrt{ LC } }
\end{split}
$$

![](images/Pasted image 20240121194639.png)



\newpage


# LCR Circuit {#lcr-circuit}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}
#important

![](images/Pasted image 20240121211020.png)

Applying KVL,
$$V = V_{R} + V_{L} + V_{C}$$

Adding them using phasors, taking current as base,
$$V = i\sqrt{ R^{2} + (X_{L} - X_{C})^{2} }$$
$$Z = \sqrt{ R^{2} + (X_{L} - X_{C})^{2} }$$

![](images/Pasted image 20240121211050.png)

##### Inductive Circuit 
The current lags voltage. 

Here, $X_{L} > X_{C}$. That is,
$$
\begin{split}
\omega L &> \frac{ 1 }{ \omega C } \\
\omega &> \frac{ 1 }{ \sqrt{ LC } }
\end{split}
$$

The resultant net voltage will be,
$$V = i\sqrt{ R^{2} + (X_{L} - X_{C})^{2} }$$

Thus, impedance is,
$$Z = \sqrt{ R^{2} + (X_{L} - X_{C})^{2} }$$

The phase difference between current and voltage,
$$
\begin{split}
\tan \theta &= \frac{ i(X_{L} - X_{C}) }{ iR } \\
&= \frac{ X_{L} - X_{C} }{ R } \\
\end{split}
$$

And power factor,
$$
\begin{split}
\cos \theta &= \frac{ V_{R} }{ V } \\
&= \frac{ iR }{ iZ } \\
&= \frac{ R }{ Z }
\end{split}
$$

![](images/Pasted image 20240121211725.png)

##### Capacitive Circuit 
The current is ahead of voltage. 

Here, $X_{L} > X_{C}$. That is,
$$
\begin{split}
\omega L &< \frac{ 1 }{ \omega C } \\
\omega &< \frac{ 1 }{ \sqrt{ LC } }
\end{split}
$$

The resultant net voltage will be,
$$V = i\sqrt{ R^{2} + (X_{C} - X_{L})^{2} }$$

Thus, impedance is,
$$Z = \sqrt{ R^{2} + (X_{C} - X_{L})^{2} }$$

The phase difference between current and voltage,
$$
\begin{split}
\tan \theta &= \frac{ i(X_{C} - X_{L}) }{ iR } \\
&= \frac{ X_{C} - X_{L} }{ R } \\
\end{split}
$$

And power factor, is the same.

![](images/Pasted image 20240121211958.png)

### Resonance
We have, 
$$i_{rms} = \frac{ V_{rms} }{ Z }$$
Thus, for max. RMS current, Z needs to be smallest. 
I.e.,
$$Z = \sqrt{ R^{2} + \left( \omega L - \frac{ 1 }{ \omega C } \right)^{2} }$$
must be smallest. 

Z will be min, (= R), when,
$$
\begin{split}
\omega L &= \frac{ 1 }{ \omega C } \\
\omega_{r} &= \frac{ 1 }{ \sqrt{ LC } }
\end{split}
$$

This angular frequency is called *resonance angular frequency.* 
And, resonance frequency is thus,
$$f_{r} = \frac{ \omega_{r} }{ 2\pi } = \frac{ 1 }{ 2\pi \sqrt{ LC } }$$

At resonance, $X_{L} = X_{C}$. 

 At resonance, the circuit is neither capacitive nor inductive, and the rms current is max. being,
 $$i_{rms} = \frac{ V_{rms} }{ R }$$

![](images/Pasted image 20240122095303.png)

#### Voltage 
Taking current as base, we add the voltages using phaser diagram. 

Here, we see that $V_{L}$ and $V_{C}$ cancel each other out, thus giving, 
$$V = V_{R} = iR$$

Thus, the circuit will behave like a purely resistive circuit at resonance and the current and applied voltage will be in the same phase. 

Power factor = 1.

![](images/Pasted image 20240122095638.png)

### Quality Factor
At resonance, average power,
$$
\begin{split}
P_{avg} &= i_{rms}V_{rms} \cos \theta \\
&= i_{rms} (i_{rms} R) \\
&= i_{rms}^{2}R
\end{split}
$$

Now, as we vary $\omega$, Z varies and thus $i_{rms}$ as well as $V_{rms}$ varies. Thus $P_{avg}$ also varies. 

We can make a curve between P and $\omega$.

![](images/Pasted image 20240122100245.png)

Half of average power can only occur at two angular frequencies, $\omega_{1}, \omega_{2}$. 

They are called *half power points.*

At max. power, $i_{rms}$ is max., and thus Z is R.

Now, at half of max. power, since $P \propto i_{rms}^{2}$, $i_{rms}$ has become $1/\sqrt{ 2 }$ its max. value,
$$i_{rms} = \frac{ i_{rms(max)} }{ \sqrt{ 2 } }$$
Thus, Z becomes,
$$
\begin{split}
Z &= \sqrt{ 2 }R \\
\sqrt{ R^{2} + (X_{L} - X_{C})^{2} } &= \sqrt{ 2 }R \\
(X_{L} - X_{C})^{2} &= R^{2}
\end{split}
$$
This will happen twice,

- **Capacitive,**

	$$
	\begin{split}
	X_{C} - X_{L} &= R \\
	\frac{ 1 }{ \omega C } - \omega L &= R \\
	1 - \omega^{2} LC &= \omega RC \\
	\omega_{1} &= \frac{ -RC + \sqrt{ R^{2} C^{2} + 4LC } }{ 2LC }
	\end{split}
	$$

- **Inductive,**

	$$
	\begin{split}
	X_{L} - X_{C} &= R \\
	\omega L - \frac{ 1 }{ \omega C } &= R \\
	\omega^{2} LC - 1 &= \omega RC \\
	\omega_{2} &= \frac{ RC + \sqrt{ R^{2} C^{2} + 4LC } }{ 2LC }
	\end{split}
	$$

The gap between these $\omega$ is $\Delta\omega$ and is called **Angular Frequency Bandwidth or Bandwidth.**

$$
\begin{split}
\Delta\omega &= \omega_{2} - \omega_{1} \\
&= \frac{ 2RC }{ 2LC } \\
&= \frac{ R }{ L }
\end{split}
$$

**Frequency Bandwidth,**
$$
\begin{split}
\Delta f &= f_{2} - f_{1} \\
&= \frac{ \Delta\omega }{ 2\pi } \\
&= \frac{ 1 }{ 2\pi } \frac{ R }{ L }
\end{split}
$$


Now, we define, **Quality Factor Q,**
$$
\begin{split}
Q &= \frac{\omega_{r}}{\Delta \omega} \\
&= \frac{ L }{ \sqrt{ LC }R } \\
&= \frac{ 1 }{ R } \sqrt{ \frac{ L }{ C } }
\end{split}
$$

Q is a unitless dimensionless quantity. It is just a ratio. 
Q decides the sharpness of $P-\omega$ graph. 

Quality Factor is also define as,
$$Q = \frac{ \text{energy stored} }{ \text{energy dissipated in 1 cycle} } \times 2\pi$$
All the quantities are at resonance. 

At resonance, both the capacitor and inductor will store the same energy, thus we can write,
$$
\begin{split}
Q &= \frac{ \frac{1}{2}Li_{rms}^{2} \times 2 }{ i_{rms}^{2} R \times \frac{2\pi}{\omega} } 2\pi \\
&= \frac{ L\omega }{ R } \\
&= \frac{ L }{ R \sqrt{ LC } } \\
&= \frac{ 1 }{ R } \sqrt{ \frac{ L }{ C } }
\end{split}
$$




\newpage


# Transformer {#transformer}
\etocsettocstyle{\textbf{Chapter Contents}\par\rule{\linewidth}{0.5pt}}{\par\rule{\linewidth}{0.5pt}}
\localtableofcontents
\noindent {}
It is used to increase or decrease the potential of an alternating current. 

It is based on the principle of mutual induction.

##### Use of Transformer 
Transformers are used in long distance transmission of electricity. 

The voltage output of the generator is stepped up and then transmitted through the wires. Since the current is reduced the energy lost in the form of heat is minimum. 

Near the consumer, it is again stepped down at the distributing substations and finally a potential of 220 V reaches our homes.

![](images/Pasted image 20240122112530.png)

#### Formation
We take a soft iron core (it has least losses) to guide the magnetic field as it is ferromagnetic. 

We take the input AC source of input emf $\varepsilon_{p}$, and wrap  primary coil of $n_{p}$ turns on one side of the core. 

As the input current is changing with time, there will be a time varying magnetic field in the core. This magnetic field is guided by the core to the secondary coil of $n_{s}$ turns. 

This secondary coil will have output emf $\varepsilon_{s}$ due to the time varying magnetic field. 

Thus the coils will have a mutual inductance.  

Now, applying KVL on the primary circuit,
$$
\begin{split}
\varepsilon_{p} - n_{p} \frac{ d\phi }{ dt } &= 0 \\
\varepsilon_{p} &= n_{p} \frac{ d\phi }{ dt }
\end{split}
$$

emf induced in the secondary coil,
$$
\begin{split}
\varepsilon_{s} &= -n_{s} \frac{ d\phi }{ dt }
\end{split}
$$
The -ve here indicates that the AC of the output and input are out of phase. I.e. $\varepsilon_{s}$ and $\varepsilon_{p}$ have a phase difference of $\pi$. 

Ratio of secondary and primary emfs is thus,
$$\frac{ \varepsilon_{s} }{ \varepsilon_{p} } = \frac{ n_{s} }{ n_{p} }$$

![](images/Pasted image 20240122130054.png)

![](images/Transformer.png)

#### Power of Ideal Transformer 
Transformer has no losses. Thus,
$$P_{in} = P_{out}$$

And we define, efficiency,
$$\eta = \frac{ P_{out} }{ P_{in} } \times 100$$
Thus, for an ideal transformer, $\eta = 100\%$

 Now, we have,
 $$
\begin{split}
P_{in} &= P_{out} \\
\varepsilon_{p} i_{p} &= \varepsilon_{s}i_{s} \\
\frac{ \varepsilon_{s} }{ \varepsilon_{p} } &= \frac{ i_{p} }{ i_{s} } \\
\frac{ n_{s} }{ n_{p} } &= \frac{ i_{p} }{ i_{s} }
\end{split} 
$$

Thus, current is inversely proportional to no. of turns. 
And, the product $\varepsilon i$ is constant.

![](images/Pasted image 20240122130834.png)

#### Step-up and Step-down transformer 
In a **step-up transformer,** the no. of turns of secondary circuit is more than that of primary circuit. Thus, the *voltage is stepped up* and *current is stepped down.*

$$
\begin{split}
n_{s} &> n_{p} \\
\varepsilon_{s} &> \varepsilon_{p} \\
i_{s} &< i_{p} 
\end{split}
$$

![](images/Pasted image 20240122131203.png)

In a **step-down transformer,** the no. of turns of primary circuit is more than that of secondary circuit. Thus, the *voltage is stepped down* and *current is stepped up.*

$$
\begin{split}
n_{s} &< n_{p} \\
\varepsilon_{s} &< \varepsilon_{p} \\
i_{s} &> i_{p} 
\end{split}
$$

![](images/Pasted image 20240122131329.png)

#### Energy Losses
There are two losses in a transformer, **copper (Cu) loss and iron (Fe) loss.** 

The *heat loss* due to resistance of (Cu) wires of the windings is called *Copper Loss.* 

$$H = i_{p}^{2}r_{p} + i_{s}^{2}r_{s}$$

Iron losses are the losses caused by the iron core of transformer. 
1. **Flux Leakage:** Not all the flux due to the first coil passes through to the second due to poor design or air gaps. It can be fixed by winding P and S one over the other. 
2. **[[00 Electromagnetic Induction#Eddy Current|Eddy Currents:]]** Alternating magnetic flux induces eddy currents in the iron core and causes heating, which dissipates energy. This can be reduced by using Laminated Core.
3. **[[07 Ferromagnetism#Hysteresis|Hysteresis:]]** Due to repeated changing of magnetic domains in the soft iron core, there will be hysteresis and thus energy loss. 


Net Power loss is,
$$
\begin{split}
\text{Power Loss} &= P_{in} - P_{out} \\
&= \varepsilon_{p}i_{p} - \varepsilon_{s}i_{s} 
\end{split}
$$

Thus, iron loss can be given as,
$$\text{Iron Loss} = (\varepsilon_{p}i_{p} - \varepsilon_{s}i_{s}) - (i_{p}^{2}r_{p} + i_{s}^{2}r_{s})$$

And efficiency will be,
$$\eta = \frac{ P_{out} }{ P_{in} } \times 100 = \frac{ \varepsilon_{s}i_{s} }{ \varepsilon_{p}i_{p} } \times 100$$


\newpage

