"""Main Graupner STDP example script"""

from __future__ import print_function

import pickle
import bluepyopt as bpop
import matplotlib.pyplot as plt
import numpy as np
import graupnerevaluator
import stdputil

cp_filename = 'checkpoints/checkpoint.pkl'

evaluator = graupnerevaluator.GraupnerEvaluator()

opt = bpop.optimisations.DEAPOptimisation(evaluator, offspring_size=100,
                                          eta=20, mutpb=0.3, cxpb=0.7)


def run_model():
    """Run model"""

    _, _, _, _ = opt.run(
        max_ngen=3000, cp_filename=cp_filename, cp_frequency=100)


def analyse():
    """Generate plot"""

    cp = pickle.load(open(cp_filename, "r"))
    results = (
        cp['population'],
        cp['halloffame'],
        cp['history'],
        cp['logbook'])

    _, hof, _, log = results

    best_ind = hof[0]
    best_ind_dict = evaluator.get_param_dict(best_ind)

    print('Best Individual')
    for attribute, value in best_ind_dict.iteritems():
        print('\t{} : {}'.format(attribute, value))

    model_sg = evaluator.compute_synaptic_gain_with_lists(best_ind)

    # Load data
    protocols, sg, _, stderr = stdputil.load_neviansakmann()
    dt = np.array([float(p.prot_id[:3]) for p in protocols])

    fig, ax = plt.subplots()

    ax.errorbar(dt, model_sg, marker='o', label='Model')
    ax.errorbar(dt, sg, yerr=stderr, marker='o', label='In vitro')

    ax.axhline(y=1, color='k', linestyle='--')
    ax.axvline(color='k', linestyle='--')

    # ax.set_xlabel(r'$\Delta t\'$(ms)')
    ax.set_ylabel('change in EPSP amplitude')
    ax.legend()

    fig.savefig('figures/graupner_fit.eps')
    plt.show()


def main():
    """Main"""
    import argparse
    parser = argparse.ArgumentParser(description='Graupner STDP')
    parser.add_argument('--start', action="store_true")
    parser.add_argument('--continue_cp', action="store_true")
    parser.add_argument('--analyse', action="store_true")

    args = parser.parse_args()
    if args.analyse:
        analyse()
    elif args.start:
        run_model()

if __name__ == '__main__':
    main()
