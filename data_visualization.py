import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from algorithms.data_generator import BogotaMedicalGenerator

def plot_with_linear_fit_and_averages():
    data = []
    generator = BogotaMedicalGenerator()
    
    for age in range(15, 81):  
        for _ in range(10):  
            height_m = generator.generate_height(age, 'M')
            data.append({'age': age, 'gender': 'M', 'height': height_m})
            height_f = generator.generate_height(age, 'F')
            data.append({'age': age, 'gender': 'F', 'height': height_f})
    
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(14, 7))
    
    for gender, color in [('M', 'blue'), ('F', 'red')]:
        gender_df = df[df['gender'] == gender]
        
        ax.scatter(gender_df['age'], gender_df['height'], 
                  alpha=0.2, color=color, label=f'{gender} (datos)')
        
        avg_heights = gender_df.groupby('age')['height'].mean()
        ax.plot(avg_heights.index, avg_heights.values, 
               color=color, linestyle='-', linewidth=3, 
               label=f'{gender} (promedio por edad)')
        
        coef = np.polyfit(gender_df['age'], gender_df['height'], 1)
        poly_fn = np.poly1d(coef)
        x_vals = np.linspace(15, 80, 100)
        ax.plot(x_vals, poly_fn(x_vals), 
               color=color, linestyle='--', linewidth=2, 
               label=f'{gender} (regresión lineal)')
        
        m, b = coef
        ax.text(81, poly_fn(80), 
               f'{gender} reg: y = {m:.3f}x + {b:.2f}', 
               color=color, va='center')

    ax.set_xlabel('Edad (años)', fontsize=12)
    ax.set_ylabel('Altura (cm)', fontsize=12)
    ax.set_title('Altura vs Edad: Promedios por Edad y Regresión Lineal', fontsize=14)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(np.arange(15, 81, 5))
    plt.tight_layout()
    plt.show()

def visualize_correlations_height_weight(n_samples=1000):
    generator = BogotaMedicalGenerator()
    ages = np.random.randint(10, 80, size=n_samples)
    heights = np.random.randint(140, 200, size=n_samples)
    sexes = np.random.choice(['M', 'F'], size=n_samples)
    weights = np.array([generator.generate_weight(age, sex, height) 
                      for age, sex, height in zip(ages, sexes, heights)])

    mask_m = sexes == 'M'
    mask_f = sexes == 'F'
    
    heights_m = heights[mask_m]
    weights_m = weights[mask_m]
    heights_f = heights[mask_f]
    weights_f = weights[mask_f]

    plt.figure(figsize=(14, 8))
    
    plt.scatter(heights_m, weights_m, c='blue', alpha=0.15, label='Hombres (datos)')
    plt.scatter(heights_f, weights_f, c='magenta', alpha=0.15, label='Mujeres (datos)')
    
    height_bins = np.arange(140, 201, 5)  

    def calculate_bin_averages(heights, weights, bins):
        bin_means = []
        bin_centers = []
        for i in range(len(bins)-1):
            mask = (heights >= bins[i]) & (heights < bins[i+1])
            if np.sum(mask) > 0: 
                bin_means.append(np.mean(weights[mask]))
                bin_centers.append((bins[i] + bins[i+1])/2)
        return np.array(bin_centers), np.array(bin_means)

    bin_centers_m, bin_means_m = calculate_bin_averages(heights_m, weights_m, height_bins)
    plt.plot(bin_centers_m, bin_means_m, 'b-o', lw=2, markersize=8, 
             label='Promedio Hombres (por 5cm)')
 
    bin_centers_f, bin_means_f = calculate_bin_averages(heights_f, weights_f, height_bins)
    plt.plot(bin_centers_f, bin_means_f, 'm-o', lw=2, markersize=8, 
             label='Promedio Mujeres (por 5cm)')

    coeff_m = np.polyfit(heights_m, weights_m, 1)
    poly_m = np.poly1d(coeff_m)
    x_vals = np.linspace(140, 200, 100)
    plt.plot(x_vals, poly_m(x_vals), 'b--', lw=2, 
             label=f'Hombres reg: y = {coeff_m[0]:.2f}x + {coeff_m[1]:.2f}')
    
    coeff_f = np.polyfit(heights_f, weights_f, 1)
    poly_f = np.poly1d(coeff_f)
    plt.plot(x_vals, poly_f(x_vals), 'm--', lw=2, 
             label=f'Mujeres reg: y = {coeff_f[0]:.2f}x + {coeff_f[1]:.2f}')

    x_ref = np.linspace(140, 200, 100)
    y_ref = x_ref - 100
    plt.plot(x_ref, y_ref, 'k:', lw=1.5, label='Referencia: Altura - 100')

    plt.xlabel('Altura (cm)', fontsize=12)
    plt.ylabel('Peso estimado (kg)', fontsize=12)
    plt.title('Relación Altura-Peso: Promedios por Bin y Regresión Lineal', fontsize=14)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()


def visualize_age_weight_averages_with_regression(samples_per_age=15):
    generator = BogotaMedicalGenerator()
    male_height = 171
    female_height = 158

    ages = np.arange(15, 91)
    all_male_weights = np.zeros((len(ages), samples_per_age))
    all_female_weights = np.zeros((len(ages), samples_per_age))

    for i, age in enumerate(ages):
        all_male_weights[i,:] = [generator.generate_weight(age, 'M', male_height) 
                               for _ in range(samples_per_age)]
        all_female_weights[i,:] = [generator.generate_weight(age, 'F', female_height) 
                                 for _ in range(samples_per_age)]

    male_avg = np.mean(all_male_weights, axis=1)
    female_avg = np.mean(all_female_weights, axis=1)

    male_ages_flat = np.repeat(ages, samples_per_age)
    male_weights_flat = all_male_weights.flatten()
    female_ages_flat = np.repeat(ages, samples_per_age)
    female_weights_flat = all_female_weights.flatten()

    plt.figure(figsize=(16, 8))

    for i, age in enumerate(ages):
        plt.scatter([age]*samples_per_age, all_male_weights[i,:], 
                   c='blue', alpha=0.15, marker='o')
        plt.scatter([age]*samples_per_age, all_female_weights[i,:], 
                   c='magenta', alpha=0.15, marker='o')

    plt.plot(ages, male_avg, 'b-', lw=3, label='Promedio Hombres (1.71m)')
    plt.plot(ages, female_avg, 'm-', lw=3, label='Promedio Mujeres (1.58m)')

    coeff_m = np.polyfit(male_ages_flat, male_weights_flat, 1)
    poly_m = np.poly1d(coeff_m)
    plt.plot(ages, poly_m(ages), 'b--', lw=2, 
            label=f'Hombres reg: y = {coeff_m[0]:.3f}x + {coeff_m[1]:.1f}')

    coeff_f = np.polyfit(female_ages_flat, female_weights_flat, 1)
    poly_f = np.poly1d(coeff_f)
    plt.plot(ages, poly_f(ages), 'm--', lw=2, 
            label=f'Mujeres reg: y = {coeff_f[0]:.3f}x + {coeff_f[1]:.1f}')

    plt.axvspan(15, 18, color='yellow', alpha=0.1, label='Edad < 18')
    plt.axvspan(60, 90, color='orange', alpha=0.1, label='Edad > 60')
    plt.axhline(male_height - 100, color='blue', linestyle=':', alpha=0.3)
    plt.axhline(female_height - 100, color='magenta', linestyle=':', alpha=0.3)

    plt.xlabel('Edad (años)', fontsize=12)
    plt.ylabel('Peso estimado (kg)', fontsize=12)
    plt.title(f'Relación Peso-Edad: Promedios y Regresión Lineal ({samples_per_age} muestras/edad)', fontsize=14)

    legend_elements = [
        Line2D([0], [0], color='blue', lw=3, label='Promedio Hombres'),
        Line2D([0], [0], color='magenta', lw=3, label='Promedio Mujeres'),
        Line2D([0], [0], color='blue', linestyle='--', lw=2, label='Regresión Hombres'),
        Line2D([0], [0], color='magenta', linestyle='--', lw=2, label='Regresión Mujeres'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, alpha=0.3, label='Datos Hombres'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='magenta', markersize=10, alpha=0.3, label='Datos Mujeres'),
        plt.Rectangle((0,0), 1, 1, fc='yellow', alpha=0.1, label='Edad < 18'),
        plt.Rectangle((0,0), 1, 1, fc='orange', alpha=0.1, label='Edad > 60'),
        Line2D([0], [0], color='blue', linestyle=':', alpha=0.3, label='Ref. Hombres (171-100)'),
        Line2D([0], [0], color='magenta', linestyle=':', alpha=0.3, label='Ref. Mujeres (158-100)')
    ]
    
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.2)
    plt.xticks(np.arange(15, 91, 5))
    plt.tight_layout()
    plt.show()

def plot_symptoms_by_age(df, figsize=(12, 6)):
    """Gráfico 1: Frecuencia de síntomas por grupo de edad"""
    fig, ax = plt.subplots(figsize=figsize)
    
    # Preparar datos
    age_bins = [10, 18, 30, 45, 60, 85]
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=['<18', '18-29', '30-44', '45-59', '60+'])
    symptom_counts = df.explode('symptoms').groupby(['age_group', 'symptoms'], observed=True).size().unstack().fillna(0)
    
    # Dibujar gráfico de barras apiladas
    bottom = np.zeros(len(symptom_counts))
    colors = plt.cm.tab20(np.linspace(0, 1, len(symptom_counts.columns)))
    
    for i, symptom in enumerate(symptom_counts.columns):
        ax.bar(symptom_counts.index.astype(str), symptom_counts[symptom], bottom=bottom, 
               label=symptom, color=colors[i])
        bottom += symptom_counts[symptom]
    
    ax.set_title('Frecuencia de Síntomas por Grupo de Edad')
    ax.set_ylabel('Frecuencia')
    ax.set_xlabel('Grupo de Edad')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Síntomas')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_diagnoses_by_bmi(df, figsize=(12, 6)):
    """Gráfico 2: Diagnósticos por categoría de BMI"""
    fig, ax = plt.subplots(figsize=figsize)
    
    diagnosis_counts = df.groupby(['bmi_category', 'diagnosis_desc'], observed=True).size().unstack().fillna(0)
    bottom = np.zeros(len(diagnosis_counts))
    colors = plt.cm.tab20(np.linspace(0, 1, len(diagnosis_counts.columns)))
    
    for i, diagnosis in enumerate(diagnosis_counts.columns):
        ax.bar(diagnosis_counts.index.astype(str), diagnosis_counts[diagnosis], bottom=bottom, 
               label=diagnosis, color=colors[i])
        bottom += diagnosis_counts[diagnosis]
    
    ax.set_title('Diagnósticos por Categoría de BMI')
    ax.set_ylabel('Frecuencia')
    ax.set_xlabel('Categoría de BMI')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Diagnósticos')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_chronic_by_bmi(df, figsize=(14, 7)):
    fig, ax = plt.subplots(figsize=figsize)
    
    chronic_data = df.explode('chronic_conditions')
    if not chronic_data.empty:
        chronic_by_bmi = chronic_data.groupby(['bmi', 'chronic_conditions'], observed=True).size().unstack().fillna(0)
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(chronic_by_bmi.columns)))
        
        for i, condition in enumerate(chronic_by_bmi.columns):
            bmi_values = chronic_by_bmi.index.values
            condition_values = chronic_by_bmi[condition].values
            
            sort_idx = np.argsort(bmi_values)
            sorted_bmi = bmi_values[sort_idx]
            sorted_values = condition_values[sort_idx]

            mask = sorted_values > 0
            if np.any(mask):
                ax.plot(sorted_bmi[mask], sorted_values[mask], 
                       color=colors[i], label=condition, linewidth=2,
                       marker='o', markersize=5, alpha=0.7)

    ax.set_title('Prevalencia de Condiciones Crónicas por BMI', fontsize=14)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.set_xlabel('Índice de Masa Corporal (BMI)', fontsize=12)

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Condiciones Crónicas')
 
    ax.axvspan(16, 18.5, color='yellow', alpha=0.1, label='Bajo peso')
    ax.axvspan(18.5, 25, color='green', alpha=0.1, label='Peso normal')
    ax.axvspan(25, 30, color='orange', alpha=0.1, label='Sobrepeso')
    ax.axvspan(30, 40, color='red', alpha=0.1, label='Obesidad')
 
    ax.set_xticks(np.arange(16, 41, 2))
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_chronic_by_age(df, figsize=(12, 6)):
    fig, ax = plt.subplots(figsize=figsize)

    chronic_data = df.explode('chronic_conditions')
    if not chronic_data.empty:
        chronic_by_age = chronic_data.groupby(['age', 'chronic_conditions'], observed=True).size().unstack().fillna(0)
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(chronic_by_age.columns)))
        
        for i, condition in enumerate(chronic_by_age.columns):
            age_values = chronic_by_age.index.values
            condition_values = chronic_by_age[condition].values

            sort_idx = np.argsort(age_values)
            sorted_age = age_values[sort_idx]
            sorted_values = condition_values[sort_idx]

            mask = sorted_values > 0
            if np.any(mask):
                ax.plot(sorted_age[mask], sorted_values[mask], 
                       color=colors[i], label=condition, linewidth=2,
                       marker='o', markersize=5, alpha=0.7)

    ax.set_title('Prevalencia de Condiciones Crónicas por Edad', fontsize=14)
    ax.set_ylabel('Frecuencia', fontsize=12)
    ax.set_xlabel('Edad (años)', fontsize=12)
 
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Condiciones Crónicas')

    ax.axvspan(10, 18, color='yellow', alpha=0.1, label='Adolescentes')
    ax.axvspan(60, 85, color='orange', alpha=0.1, label='Adultos mayores')
  
    ax.set_xticks(np.arange(10, 86, 5))
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def plot_symptoms_count(df, figsize=(14, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    
    cmap = plt.cm.get_cmap('plasma')  
    norm = plt.Normalize(df['num_symptoms'].min(), df['num_symptoms'].max())

    for num in sorted(df['num_symptoms'].unique()):
        subset = df[df['num_symptoms'] == num]
        if not subset.empty:
            size = 50 + num * 30  
            ax.scatter(
                subset['age'], 
                subset['bmi'], 
                c=cmap(norm(num)), 
                s=size, 
                alpha=0.7,  
                edgecolors='w',  
                linewidth=0.5,  
                label=f'{num} síntoma(s)' if num == 1 else f'{num} síntomas'
            )
    
    ax.set_title('Relación entre Edad, BMI y Número de Síntomas', fontsize=16, pad=20)
    ax.set_xlabel('Edad (años)', fontsize=12)
    ax.set_ylabel('Índice de Masa Corporal (BMI)', fontsize=12)

    ax.axhline(y=18.5, color='yellow', linestyle='--', alpha=0.5, linewidth=1)
    ax.axhline(y=25, color='green', linestyle='--', alpha=0.5, linewidth=1)
    ax.axhline(y=30, color='orange', linestyle='--', alpha=0.5, linewidth=1)

    legend = ax.legend(
        bbox_to_anchor=(1.05, 1), 
        loc='upper left', 
        title='Número de Síntomas',
        frameon=True,
        framealpha=0.9
    )
    legend.get_title().set_fontsize(11)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label('Número de Síntomas', rotation=270, labelpad=15)
    
    ax.set_xticks(np.arange(df['age'].min(), df['age'].max()+1, 5))
    ax.set_yticks(np.arange(15, 41, 5))
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.show()

def generate_medical_data(generator, n_samples=1000):
    data = []
    for _ in range(n_samples):
        age = np.random.randint(15, 85)
        bmi = round(np.random.uniform(16, 40), 1)
        symptoms, diagnosis, chronic = generator.generate_symptoms_diagnosis(age, bmi)
        data.append({
            'age': age,
            'bmi': bmi,
            'bmi_category': generator.get_bmi_category(bmi),
            'symptoms': symptoms,
            'diagnosis_code': diagnosis[0],
            'diagnosis_desc': diagnosis[1],
            'chronic_conditions': chronic,
            'num_symptoms': len(symptoms),
            'has_chronic': len(chronic) > 0
        })
    return pd.DataFrame(data)

def generate_graphics():
    generator = BogotaMedicalGenerator()
    df = generate_medical_data(generator, n_samples=50000)

    plot_with_linear_fit_and_averages()
    visualize_correlations_height_weight()
    visualize_age_weight_averages_with_regression()
    plot_symptoms_by_age(df)
    plot_diagnoses_by_bmi(df)
    plot_chronic_by_bmi(df)
    plot_chronic_by_age(df)
    plot_symptoms_count(df)