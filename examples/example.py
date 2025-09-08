#!/usr/bin/env python3
"""
Example usage of the Lexical Analyzer.

This script demonstrates how to use the LexicalAnalyzer class
programmatically to process regular expressions.
"""

from lexical_analyzer import LexicalAnalyzer


def main():
    """Main example function."""
    print("🚀 Lexical Analyzer Example")
    print("=" * 40)
    
    # Initialize analyzer
    analyzer = LexicalAnalyzer(eps_symbol="ε")
    
    # Example regular expressions and test words
    examples = [
        ("(a|b)*abb", "aabb"),
        ("a*b*", "aabbb"),
        ("(ab)*", "abab"),
        ("a+", "aaa"),
        ("a?", "a"),
        ("a?", ""),  # Empty string
    ]
    
    for i, (regex, test_word) in enumerate(examples, 1):
        print(f"\n📝 Example {i}:")
        print(f"   Regex: {regex}")
        print(f"   Test word: '{test_word}'")
        
        try:
            # Process the regular expression
            result = analyzer.process_regex(
                regex_raw=regex,
                test_word=test_word,
                output_dir=f"./example_output_{i}",
                ascii_eps=True
            )
            
            # Display results
            print(f"   ✅ Processing completed!")
            print(f"   📊 Postfix: {result.postfix}")
            print(f"   🔢 States: NFA={result.nfa_states}, DFA={result.dfa_states}, Min={result.dfa_min_states}")
            print(f"   ✅ Accepts '{test_word}': NFA={'Yes' if result.nfa_accepts else 'No'}, "
                  f"DFA={'Yes' if result.dfa_accepts else 'No'}, "
                  f"Min={'Yes' if result.dfa_min_accepts else 'No'}")
            print(f"   📁 Files generated in: ./example_output_{i}/")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Example completed!")
    print(f"💡 Try running: lexical-analyzer --help")


if __name__ == "__main__":
    main()
