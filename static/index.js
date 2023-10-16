document.addEventListener('DOMContentLoaded', function () {
            var srcElements = document.getElementsByClassName("m2");
            const array = Array.from(srcElements);
            
            array.forEach(function (element) {
                var text = element.textContent;
                var words = text.split(' ');
                words.forEach(function (word, index) {
                    if (word.includes('+++')) {
                        words[index] = '<span style="background-color: yellowgreen;">' + word.replace("+++","") + '</span>';
                    }
                    if (word.includes('---')) {
                        words[index] = '<span style="background-color: pink;">' + word.replace("---", "") + '</span>';
                    }
                });

                var coloredText = words.join(' ');
                element.innerHTML = coloredText;
            });
        });