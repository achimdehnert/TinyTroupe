# TinyTroupe Group Discussion Framework

A powerful and flexible framework for conducting AI-powered group discussions, interviews, brainstorming sessions, and evaluations using the TinyTroupe library.

## 🌟 Features

- **Multiple Discussion Types**
  - Focus Groups
  - One-on-One Interviews
  - Product Brainstorming
  - Advertisement Evaluation
  - Custom Discussions

- **Smart Agent Management**
  - Pre-configured expert agents
  - Custom agent generation
  - Dynamic agent interactions

- **Flexible Data Extraction**
  - Configurable extraction objectives
  - Multiple output formats
  - Result reduction capabilities

- **Integrated Storage**
  - File-based storage (JSON)
  - Database integration (MySQL & PostgreSQL)
  - Rich metadata support

## 🚀 Quick Start

```python
from group_discussion import ApartmentAdDiscussion, ProductBrainstormingDiscussion

# Example 1: Run a focus group for apartment advertising
apartment_desc = """
Modern 1-bedroom apartment, fully renovated with integrated spaces.
Close to medical school and public transport.
"""
discussion = ApartmentAdDiscussion(apartment_desc)
results = discussion.run_discussion()
discussion.save_results(results, "data/extractions/apartment_ad.json")

# Example 2: Brainstorm product features
brainstorm = ProductBrainstormingDiscussion("Microsoft Word", "office productivity")
results = brainstorm.run_discussion(num_steps=4)
brainstorm.save_results(results, "data/extractions/word_features.json")
```

## 📦 Installation

1. Ensure you have Python 3.7+ installed
2. Install required dependencies:
```bash
pip install -r requirements.txt
```
3. Set up your database configuration in `.env`

## 📚 Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

## 🎯 Use Cases

1. **Product Development**
   - Feature brainstorming
   - User feedback analysis
   - Market research

2. **Marketing**
   - Ad copy creation
   - Campaign evaluation
   - Target audience research

3. **Customer Research**
   - Customer interviews
   - Pain point analysis
   - Need identification

4. **Content Creation**
   - Copy evaluation
   - Content ideation
   - Message testing

## 🔜 Roadmap

- [ ] Add support for more discussion types
- [ ] Implement real-time discussion analysis
- [ ] Add export to different formats (PDF, DOCX)
- [ ] Create web interface for discussion management
- [ ] Add support for multi-language discussions
- [ ] Implement discussion templates system

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [TinyTroupe](https://github.com/yourusername/TinyTroupe)
- Inspired by real-world focus group methodologies
